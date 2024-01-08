import cv2
import numpy as np
from ultralytics import YOLO
from ripness_detection import calculate_percent_in_mask

def load_model(model_path):
    # Load YOLOV8 ONNX
    return YOLO(model_path, task='segment')

# load video
def load_video(video_path):
    return cv2.VideoCapture(video_path)

def extract_contour_and_mask(c):
    contour = c.masks.xy.pop()
    contour = contour.astype(np.int32)
    contour = contour.reshape(-1, 1, 2)

    # Draw contour onto mask
    b_mask = np.zeros(c.orig_img.shape[:2], np.uint8)
    _ = cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)

    mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)

    return b_mask, mask3ch

def find_strawberry(frame, model):
    results = model(frame, conf=0.9)
    red_color_percent = 0
    green_color_percent = 0

    if results[0].boxes is not None:
        for result in results:
            img = result.orig_img
            for ci, c in enumerate(result):
                label = c.names[c.boxes.cls.tolist().pop()]
                _, mask3ch = extract_contour_and_mask(c)
                
                isolated = cv2.bitwise_and(mask3ch, img)
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)

                iso_crop = isolated[y1:y2, x1:x2]
                mask_crop = mask3ch[y1:y2, x1:x2]
                red_color_percent, green_color_percent = calculate_percent_in_mask(iso_crop, mask_crop)

    return red_color_percent, green_color_percent, results[0].plot()

def process_frame(frame, mask, frame_width, frame_height, model):
    #Check if mask size is same as frame size
    
    mask = cv2.resize(mask, (frame_width, frame_height))
    # Apply bitwise AND operation
    result = cv2.bitwise_and(frame, mask)

    return find_strawberry(result, model)


