import cv2
import time
from ultralytics import YOLO
from utils.utils import calculate_centroid


window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

def show_camera():
    
    model = YOLO('model/segment/best.pt', task='segment')

    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(0)
    #Init Mask
    #mask = cv2.imread('mask.png')
    #Reize Mask to H 480 W 640
    #mask = cv2.resize(mask, (640, 480))
    prev_frame_time = 0
    new_frame_time = 0
    if video_capture.isOpened():
        try:
            while True:
                _, frame = video_capture.read()
                #Bitwise And Mask
                #frame = cv2.bitwise_and(frame, mask)

                #Run Model
                results = model(frame, conf=0.7, half=True, device=0)       
                cv2.imshow(window_title, frame)
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
