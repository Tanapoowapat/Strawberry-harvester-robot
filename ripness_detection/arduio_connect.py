import time
import serial
import queue

class Arduino:
    def __init__(self, port, baud_rate, timeout) -> None:
        self.received_data_queue = queue.Queue()
        self.arduino = serial.Serial(port, baud_rate, timeout)
        
    def send_data(self, data):
        data = f"{data}\n"
        self.write(data.encode())
        time.sleep(1)  # Ensure Arduino has time to process data
        return True

    def callback(self):
        while True:
            time.sleep(0.5)
            received_data = self.readline().decode('utf8').strip()
            if received_data:
                self.received_data_queue.put(received_data)
            