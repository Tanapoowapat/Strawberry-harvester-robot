import cv2
from ultralytics import YOLO
import time
prev_frame_time = 0
new_frame_time = 0

global WINDOW_TITLE
WINDOW_TITLE = "Strawberry Ripeness Detection"
#LOAD MODEL
model = YOLO('model/detection/best.pt')
#LOAD WEBCAM 1 OR 0 for default webcam
cap = cv2.VideoCapture(0)
#READ THE FRAME
if cap.isOpened():
    try:
        
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
                print(result)
                frame = result.plot()
                cv2.imshow('frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
else:
    print("Error: Could not open webcam.")