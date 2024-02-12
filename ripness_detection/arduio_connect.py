import serial
import time

def send_data_to_arduino(py, arduino):
    data = f"{py}\n"
    arduino.write(data.encode())
    time.sleep(0.1)

def send_data(py):
    arduino_port = '/dev/ttyACM0'
    baud_rate = 9600
    arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)
    
    send_data_to_arduino(py)
    while True:
        received_data = arduino.readline().decode('utf8').strip()
        print(received_data)
        if received_data == "succeed":
            return received_data
    