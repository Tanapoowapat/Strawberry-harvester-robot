import time
from process import find_strawberry
import cv2
from ultralytics import YOLO


window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

def show_camera(model):
    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    
    prev_frame_time = 0
    new_frame_time = 0
    if video_capture.isOpened():
        try:
            while True:
                _, frame = video_capture.read()
                
                #CALCULATE FPS
                new_frame_time = time.time()
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)
                print(f'FPS :  {str(fps)}')
                
                results = model(frame, stream=True, conf=0.9, half=True, device=0)
                for result in results:
                    ripness, boxes = find_strawberry(result)
                    if boxes is not None and ripness is not None:
                        x1, x2 = boxes[0], boxes[2]
                        print(f'Ripness: {ripness} | x1 : {x1} | x2 : {x2}')

                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        except Exception as e:
            print(e)
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    print('Load Model...')
    model = YOLO('model/segment/best.engine', task='segment')
    show_camera(model)
