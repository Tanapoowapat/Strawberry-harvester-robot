import cv2
import threading
from ultralytics import YOLO
from arduio_connect import send_data_to_arduino, arduino_receive_callback, received_data_queue, arduino
from process import process_frame


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

def process_results(results):
    """Process the results of frame analysis."""
    for result in results:
        py = process_frame(result)
        if py is not None:
            for _, pos_y in enumerate(py):
                pos_y = 16 + (10 - (pos_y * 0.0264583333))
                if pos_y >= 22 or pos_y <= 11:
                    print("Error: Invalid position")
                    return None
                return pos_y

def show_camera(model):
    """Display camera feed and send data to Arduino."""
    COUNT = 0
    model(source='test_image/14.png', conf=0.9, half=True, device=0)  # Warm up model.

    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
    mask = cv2.imread('mask.png')

    #Send data to Arduino to start motor
    send_data_to_arduino("start")

    if video_capture.isOpened():
        
        arduino_receive_thread = threading.Thread(target=arduino_receive_callback, args=(arduino,))
        arduino_receive_thread.daemon = True
        arduino_receive_thread.start()

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Unable to read frame from camera")
                break
            
            if not received_data_queue.empty():
                received_data = received_data_queue.get()
                print("Data received in show_camera function:", received_data)
                # if data == "finish" then stop capturing frames stop
                if received_data == "finish":
                    close_camera(video_capture)
                    break

            if COUNT >= 50:
                send_data_to_arduino("finish")
                break

            frame = cv2.bitwise_and(frame, mask)
            results = model(frame, stream=True, conf=0.5, half=True, device=0)
            pos_y = process_results(results)

            # Send data to Arduino
            if pos_y is not None:
                close_camera(video_capture)
                status = send_data_to_arduino(pos_y)
                if status:
                    print("Data sent to Arduino...")
                    while received_data_queue.empty():
                        pass
                    if received_data_queue.get() == "success":
                        print("Data received by Arduino...")
                        COUNT += 1
                        video_capture = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
                    else:
                        print("Error: Unable to received data from Arduino")
                else:
                    print("Error: Unable to send data to Arduino")
            
            # Display the captured frame
            cv2.imshow(WINDOW_TITLE, frame)
            keyCode = cv2.waitKey(10) & 0xFF
            if keyCode == 27 or keyCode == ord('q'):
                break
            
    else:
        print("Error: Unable to open camera")

    close_camera(video_capture)

def start_process():
    """Load YOLO model and start camera processing."""
    print('Load Model...')
    model = YOLO('model/segment/best.engine', task='segment')
    show_camera(model)

start_process()
