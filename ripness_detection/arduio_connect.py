import serial
import time

def send_data_to_arduino(py, arduino):
    py = int(py)
    print(f'{py} sent to arduino...')
    data = f"{py}\n"
    arduino.write(data.encode())
    time.sleep(0.1)

def send_data(py):
    if py > 21  or py < 11:
        print('Invalid data')
    else:
        arduino_port = '/dev/ttyACM0'
        baud_rate = 9600
        arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)
        
        send_data_to_arduino(py, arduino)
        while True:
            received_data = arduino.readline().decode('utf8').strip()
            print(received_data)
            if received_data == "succeed":
                break
