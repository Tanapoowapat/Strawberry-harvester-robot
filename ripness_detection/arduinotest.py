import serial
import time
import threading
import queue

received_data_queue = queue.Queue()
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_data_to_arduino(data):
    data = f"{data}\n"
    arduino.write(data.encode())
    time.sleep(1)  # Ensure Arduino has time to process data
    return True


def arduino_receive_callback(arduino):
    while True:
        time.sleep(0.5)
        received_data = arduino.readline().decode('utf8').strip()
        if received_data:
            received_data_queue.put(received_data)

def main():
    #send stop to arduino
    send_data_to_arduino("stop")
    # Start a thread to receive data from Arduino
    print('Start Arduino receive thread...')
    arduino_receive_thread = threading.Thread(target=arduino_receive_callback, args=(arduino,))
    arduino_receive_thread.daemon = True
    arduino_receive_thread.start()

    #receive data from queue
    while True:
        if not received_data_queue.empty():
            received_data = received_data_queue.get()
            print("Data received in show_camera function:", received_data)
            time.sleep(5)
            break