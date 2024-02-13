import serial
import time
import queue

received_data_queue = queue.Queue()

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

while True:
    received_data = arduino.readline().decode('utf8').strip()
    if received_data:
        print("Received data from Arduino:", received_data)
        received_data_queue.put(received_data)
        if received_data == "finish":
            break