import time
import serial
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
            print("Received data from Arduino:", received_data)
            received_data_queue.put(received_data)
            