from process import find_strawberry, process_frame
import cv2
from ultralytics import YOLO
from utils.utils import fps

window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

def show_camera(model):
    
    _ = model(source='test_image/14.png', conf=0.9, half=True, device=0)  # Warm up model.
    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    #video_capture = cv2.VideoCapture(1)
    mask = cv2.imread('mask.png')
    prev_frame_time = 0
    new_frame_time = 0
    if video_capture.isOpened():
        try:
            while True:
                _, frame = video_capture.read()
                # Bitwise-AND mask into frame.
                frame = cv2.bitwise_and(frame, mask)
                results = model(frame, stream=True, conf=0.5, half=True, device=0)  
                #CALCULATE FPS
                prev_frame_time = fps(new_frame_time, prev_frame_time)
                for result in results:
                    process_frame(frame ,result)
                frame = result.plot()
                cv2.imshow(window_title, frame)
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
