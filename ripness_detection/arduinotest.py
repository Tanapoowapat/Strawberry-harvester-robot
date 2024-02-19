import threading
import time
from arduio_connect import send_data_to_arduino, arduino_receive_callback, received_data_queue, arduino


def main():

    # Start a thread to receive data from Arduino
    print('Start Arduino receive thread...')
    arduino_receive_thread = threading.Thread(target=arduino_receive_callback, args=(arduino,))
    arduino_receive_thread.daemon = True
    arduino_receive_thread.start()

    while True:
        if not received_data_queue.empty():
            received_data = received_data_queue.get() 
            print("Data received in show_camera function:", received_data)
            if received_data == "success":
                print("Success")
                time.sleep(1)
                continue
            if received_data == "finish":
                print("Finish")
                time.sleep(1)
                continue
            if received_data == "start":
                print("Start")
                time.sleep(1)
                continue
if __name__ == "__main__":
    main()