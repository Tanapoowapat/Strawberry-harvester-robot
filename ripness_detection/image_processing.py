import cv2
import threading
from ultralytics import YOLO
from arduio_connect import (
    send_data_to_arduino,
    arduino_receive_callback,
    received_data_queue,
    arduino
)
from process import process_frame
from utils.utils import fps

# Constants
WINDOW_TITLE = "USB Camera"
PIPELINE = " ! ".join([
    "v4l2src device=/dev/video0",
    "video/x-raw, width=640, height=480, framerate=30/1",
    "videoconvert",
    "video/x-raw, format=(string)BGR",
    "appsink"
])

def close_camera(cap):
    """Release the camera and close any OpenCV windows."""
    cap.release()
    cv2.destroyAllWindows()

def start_arduino_receive_thread():
    """Start a thread to receive data from Arduino."""
    print('Start Arduino receive thread...')
    arduino_receive_thread = threading.Thread(target=arduino_receive_callback, args=(arduino,))
    arduino_receive_thread.daemon = True
    arduino_receive_thread.start()

def start_motor():
    """Start the motor."""
    print('Start Motor...')
    send_data_to_arduino("start")

def show_camera(model, ripeness):
    """Display camera feed and send data to Arduino."""
    COUNT = 0

    # Initialize video capture and mask
    video_capture = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
    print('Start Reading Camera...')
    mask = cv2.imread("mask.png")
    MOTOR = False

    if video_capture.isOpened():
        close_camera(video_capture)
        start_arduino_receive_thread()

        while True:
            _, frame = video_capture.read()
            frame = cv2.bitwise_and(frame, mask)

            if not MOTOR:
                start_motor()
                MOTOR = True
                
            # Check if received data from Arduino
            if not received_data_queue.empty():
                received_data = received_data_queue.get() 
                if received_data == 'close':
                    # Close the camera
                    close_camera(video_capture)
                    # Process incoming messages until 'open' or 'finish' is received
                    while True:
                        data = received_data_queue.get() 
                        if data == "open":
                            print(data)
                            # Reopen the camera
                            video_capture = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
                            break
                        elif data == 'finish':
                            print(data)
                            # Close the camera and return the count
                            close_camera(video_capture)
                            return COUNT
                        
            # If more than 50 strawberries are detected
            if COUNT >= 50:
                send_data_to_arduino("full")
                close_camera(video_capture)
                return COUNT
            # predict the video frame
            results = model(frame, stream=True, conf=0.2, device=0)
            _, show_fps = fps()
            print("FPS:", show_fps)
            
            #If found Strawberry
            for result in results:
                py = process_frame(result, ripeness)
                if py is not None:
                    for pos_y in py:
                        if pos_y >= 22 or pos_y <= 11:
                            print(f"Error: Invalid position {pos_y}")
                        else:
                            print(pos_y)
                            close_camera(video_capture)
                            status = send_data_to_arduino(pos_y)
                            if status:
                                print("Data sent to Arduino...")
                                while received_data_queue.empty():
                                    pass
                                if received_data_queue.get() == "success":
                                    print(f'Position {pos_y} sent to Arduino successfully')
                                    COUNT += 1
                                    print(COUNT)
                                    video_capture = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
                            else:
                                print("Error: Unable to send data to Arduino")
                    else:
                        pass

            keyCode = cv2.waitKey(10) & 0xFF
            if keyCode == 27 or keyCode == ord('q'):
                send_data_to_arduino("stop")
                MOTOR = False
                break
            
    else:
        print("Error: Unable to open camera")

    close_camera(video_capture)

def start_process(ripeness):
    """Load YOLO model and start camera processing."""
    print('Load Model...')
    model = YOLO('model/segment/best.engine', task='segment')
    show_camera(model, ripeness)
