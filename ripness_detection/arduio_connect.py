import serial
import time

def send_data_to_arduino(py, arduino):
    print(f'{py}')
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
            print('Receiving data from arduino...')
            received_data = arduino.readline().decode('utf8').strip()
            if received_data == "succeed":
                break
