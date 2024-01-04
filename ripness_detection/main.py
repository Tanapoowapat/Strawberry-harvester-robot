import cv2
import numpy as np
from ultralytics import YOLO
from utils.utils import crops_image



video_path = "test_image/test.mp4"

if __name__ == "__main__":
    # Load YOLOV8 ONNX
    model = YOLO("model/best.onnx", task='segment')
    
    #Load Video mp4
    cap = cv2.VideoCapture(video_path)

    ret = True

    while ret:
        ret, frame = cap.read()

        if ret:

            #detect object and track
            result = model(frame, vid_stride=True, stream_buffer=True)
            
            #plot result
            frame_ = result[0].plot()

            #visualize
            cv2.imshow('frame', frame_)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
