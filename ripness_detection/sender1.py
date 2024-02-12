import serial
import time

arduino_port = '/dev/ttyACM0'
baud_rate = 9600
arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_data_to_arduino(py):
    data = f"{py}\n"
    arduino.write(data.encode())
    time.sleep(0.1)

while True:
    py = float(input("Enter py: "))
    send_data_to_arduino(py)

    while True:
        received_data = arduino.readline().decode('utf8').strip()
        print(received_data)
        if received_data == "succeed":
            break