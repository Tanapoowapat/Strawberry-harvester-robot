from process import process_frame
import cv2
from ultralytics import YOLO
from utils.utils import fps
import serial
import time
window_title = "USB Camera"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_data_to_arduino(pos_y, cap):
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close any OpenCV windows
    data = f"{pos_y}\n"
    arduino.write(data.encode())
    time.sleep(0.1)  # Ensure Arduino has time to process data
    received_data = ""
    while received_data != "succeed":
        received_data = arduino.readline().decode('utf8').strip()
        if received_data:
            print("Received data from Arduino:", received_data)
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)  # Reopen the camera
    return received_data, cap

def show_camera(model):
    _ = model(source='test_image/14.png', conf=0.9, half=True, device=0)  # Warm up model.
    print('Start Reading Camera...')
    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    mask = cv2.imread('mask.png')
    if video_capture.isOpened():
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Unable to read frame from camera")
                break

            frame = cv2.bitwise_and(frame, mask)
            results = model(frame, stream=True, conf=0.5, half=True, device=0)  

            for result in results:
                py = process_frame(result)
                if py is not None:
                    for _, pos_y in enumerate(py):
                            pos_y = 16 + (10-(pos_y*0.0264583333))
                            print(pos_y)
                            if pos_y >= 22 or pos_y <= 11:
                                print("Error: Invalid position")
                                break
                            status, video_capture = send_data_to_arduino(pos_y, video_capture)
                            if status == "succeed":
                                print("Data sent successfully")
                            else:
                                print("Error sending data to Arduino")
                                break

            cv2.imshow(window_title, frame)
            keyCode = cv2.waitKey(10) & 0xFF
            if keyCode == 27 or keyCode == ord('q'):
                break
    else:
        print("Error: Unable to open camera")

    video_capture.release()
    cv2.destroyAllWindows()

def start_process():
    print('Load Model...')
    model = YOLO('model/segment/best.engine', task='segment')
    show_camera(model)

start_process()