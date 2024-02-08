import sys
import cv2
from ultralytics import YOLO
import time
prev_frame_time = 0
new_frame_time = 0

global WINDOW_TITLE
WINDOW_TITLE = "Strawberry Ripeness Detection"

pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

#LOAD MODEL
model = YOLO('model/detection/best.pt')
#LOAD WEBCAM 1 OR 0 for default webcam
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
#READ THE FRAME
if cap.isOpened():
    try:
        window_title = cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_AUTOSIZE)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            
            #PROCESS THE FRAME
            results = model(frame, stream=True, half=True, conf=0.9)

            #CALCULATE FPS
            new_frame_time = time.time() 
            fps = 1/(new_frame_time-prev_frame_time) 
            prev_frame_time = new_frame_time 
            fps = int(fps) 
            fps = str(fps)

            cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX , 3, (100, 255, 0), 3, cv2.LINE_AA) 


            #DISPLAY THE FRAME
            for result in results:
                frame = result.plot()
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) >= 0:
                cv2.imshow('frame', frame)
            else:
                break
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
else:
    print("Error: Could not open webcam.")