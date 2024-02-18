from ultralytics import YOLO
from utils.utils import fps
import numpy as np
from process import process_frame
import cv2


new_frame_time = 0
prev_frame_time = 0

video = 0
model = YOLO('model/test_model/best.engine', task='segment')

def corp_result(x1, y1, x2, y2):
    return img[y1:y2, x1:x2]


def color_calculator(crop_frame):
#convert to RGB
            crop_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2HSV)
            #mask for red color
            lower_red = np.array([0, 40, 50])
            upper_red = np.array([15, 255, 255])
            mask0 = cv2.inRange(crop_frame, lower_red, upper_red)
            
            lower_red = np.array([160, 40, 50])
            upper_red = np.array([180, 255, 255])
            mask1 = cv2.inRange(crop_frame, lower_red, upper_red)

            maskRed = mask0 + mask1

            #mask for green color
            lower_green = np.array([20,40,50])
            upper_green = np.array([80,255,255])
            maskGreen = cv2.inRange(crop_frame, lower_green, upper_green)

            #calculate the percentage of red and green color
            red_color_percent = cv2.countNonZero(maskRed) / cv2.countNonZero(maskRed + maskGreen) * 100
            green_color_percent = cv2.countNonZero(maskGreen) / cv2.countNonZero(maskRed + maskGreen) * 100

            return red_color_percent, green_color_percent

def ripness_calculate(red_percent, green_percent):
    if red_percent >= 80 and green_percent < 10:
        return 'FullRipe'
    elif 80 < red_percent >= 70 and green_percent < 20:
        return 'Ripe'
    elif 70 < red_percent >= 50 and green_percent < 40:
        return 'MediumRipe'
    elif 50 < red_percent >= 30 and green_percent < 60:
        return 'SmallRipe'
    elif 30 < red_percent >= 10 or green_percent < 80:
        return 'Unripe'

def calculate_center_xy(x1, y1, x2, y2):
    center_xy = (int((x1+x2)/2), int((y1+y2)/2)-80)
    return center_xy

# PIPELINE = " ! ".join([
#     "v4l2src device=/dev/video0",
#     "video/x-raw, width=640, height=480, framerate=30/1",
#     "videoconvert",
#     "video/x-raw, format=(string)BGR",
#     "appsink"
# ])


# cap = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)

cap = cv2.VideoCapture(0)
mask = cv2.imread("mask.png")
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.bitwise_and(frame, mask)
    if not ret:
        break
    
    results = model(frame, conf=0.2, iou=0.5, half=True,  stream=True)
    prev_frame_time, frame_per_sec = fps(new_frame_time, prev_frame_time)
    
    for result in results:
        img = result.orig_img
        for _, c in enumerate(result):
            x1, y1, x2, y2 = c.boxes.xyxy[0].cpu().numpy().astype(np.int32)
            crop_frame = corp_result(x1, y1, x2, y2)
            red_color_percent, green_color_percent = color_calculator(crop_frame)
            ripeness = ripness_calculate(red_color_percent, green_color_percent)
            center_xy = calculate_center_xy(x1, y1, x2, y2)
            
            #Draw text of center_xy on bbox

            cv2.putText(img, str(center_xy), (x1, y1-70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 5)
            cv2.circle(img, center_xy, 5, (0, 255, 0), 2)
            cv2.putText(img, ripeness, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'Red : {red_color_percent:.2f}%', (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, f'Green : {green_color_percent:.2f}%', (x1, y1-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
                        


    cv2.putText(img, f'{frame_per_sec:.2f} FPS', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame', img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break