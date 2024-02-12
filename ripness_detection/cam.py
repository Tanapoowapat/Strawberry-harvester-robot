import cv2
import time
from ultralytics import YOLO
from utils.utils import calculate_centroid
# ASSIGN CAMERA ADRESS to DEVICE HERE!
# pipeline = " ! ".join(["v4l2src device=/dev/video0",
#                        "video/x-raw, width=640, height=480, framerate=30/1",
#                        "videoconvert",
#                        "video/x-raw, format=(string)BGR",
#                        "appsink"
#                        ])

def close_webcam(cap):
    # Release the VideoCapture object
    cap.release()
    print('Camera released...')


def open_webcam(pipeline):
    # Create a VideoCapture object with Gstreamer pipeline
    cap = cv2.VideoCapture(pipeline)
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return None
    return cap



def show_camera(pipeline):
    global running
    running = True
    cap = open_webcam(pipeline)
    if cap is None:
        return

    print('Start Reading Camera...')
    
    while True:
        if running:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            # Display the captured frame
            cv2.imshow('Webcam', frame)
        

        
        keyCode = cv2.waitKey(10) & 0xFF
        if keyCode == 27 or keyCode == ord('q'):
            close_webcam()
            cv2.destroyAllWindows()
            break
        
    close_webcam(cap)

def start_process():
    print('Load Model...')
    show_camera(0)

start_process()