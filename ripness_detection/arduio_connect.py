import time
import serial

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_data_to_arduino(data):
    data = f"{data}\n"
    arduino.write(data.encode())
    time.sleep(0.5)  # Ensure Arduino has time to process data
    return True

def arduino_receive(arduino):
    while True:
        received_data = arduino.readline().decode('utf8').strip()
        if received_data:
            print("Received data from Arduino:", received_data)
            return received_data
