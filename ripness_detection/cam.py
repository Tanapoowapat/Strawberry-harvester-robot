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
import threading
import queue
import serial


received_data_queue = queue.Queue()

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_data_to_arduino(data):
    data = f"{data}\n"
    arduino.write(data.encode())
    time.sleep(0.5)  # Ensure Arduino has time to process data
    return True

def arduino_receive_callback(arduino):
    while True:
        received_data = arduino.readline().decode('utf8').strip()
        if received_data:
            print("Received data from Arduino:", received_data)
            received_data_queue.put(received_data)



def close_webcam(cap):
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
    print('Camera released...')


def open_webcam(pipeline):
    # Create a VideoCapture object with Gstreamer pipeline
    cap = cv2.VideoCapture(pipeline)
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return None
    return cap

def show_camera(pipeline):
    cap = open_webcam(pipeline)
    if cap is None:
        return
    
    arduino_receive_thread = threading.Thread(target=arduino_receive_callback, args=(arduino,))
    arduino_receive_thread.daemon = True
    arduino_receive_thread.start()

    print('Start Reading Camera...')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        # Display the captured frame
        cv2.imshow('Webcam', frame)

        if not received_data_queue.empty():
                received_data = received_data_queue.get()
                # Process received data here as needed
                print("Data received in show_camera function:", received_data)    
                if received_data == "finish":
                    close_webcam(cap)
                    break


        
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