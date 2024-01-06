import cv2
import numpy as np
from ultralytics import YOLO
from ripness_detection import calculate_percent_in_mask


def load_model():
    # Load YOLOV8 ONNX
    return YOLO("model/best.onnx", task='segment')

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

def process_frame(frame, model):
    results = model(frame, vid_stride=True, stream_buffer=True)

    for result in results:
        img = result.orig_img
        for ci, c in enumerate(result):
            label = c.names[c.boxes.cls.tolist().pop()]
            b_mask, mask3ch = extract_contour_and_mask(c)

            isolated = cv2.bitwise_and(mask3ch, img)
            x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)

            iso_crop = isolated[y1:y2, x1:x2]
            mask_crop = mask3ch[y1:y2, x1:x2]
            red_color_percent, green_color_percent = calculate_percent_in_mask(iso_crop, mask_crop)

    return red_color_percent, green_color_percent, results[0].plot()