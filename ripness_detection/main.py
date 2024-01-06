import cv2
import numpy as np
from ultralytics import YOLO
from process import load_model, load_video, process_frame


video_path = "test_image/test.mp4"
model_path = 'model/best.onnx'

def main():
    
    model = load_model(model_path)
    cap = load_video(video_path)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        red_percent, green_percent, frame_ = process_frame(frame, model)

        print(f'Red : {red_percent}, Green : {green_percent}')

        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()