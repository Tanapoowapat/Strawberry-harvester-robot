import paho.mqtt.client as mqtt
import time
import json
import threading
import sys
from image_processing import start_process

def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the broker."""
    client.subscribe("user/input")
    if rc == 0:
        client.publish("sys_nano/status", 1)
        print("======================\nConnected successfully\n======================")
    else:
        client.publish("sys_nano/status", 3)
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    """Callback function for when the client receives a message."""
    received_data = msg.payload
    json_data = json.loads(received_data)
    ch = json_data.get('ripeness')

    if ch == 'q':
        print('Received "q". Stopping the program.')
        client.publish("sys_nano/status", 3)
        client.disconnect()
    elif 'ripeness' in json_data:
        client.publish("sys_nano/status", 2)
        time.sleep(1)
        ripeness_level = {
            1: 'Unripe',
            2: 'SmallRipe',
            3: 'MediumRipe',
            4: 'Ripe',
            5: 'FullRipe'
        }.get(json_data['ripeness'])

        if ripeness_level is not None:
            print(f'{ripeness_level}')
            strawbery_count = start_process(ripeness_level)
            print(strawbery_count)
            client.publish("sys_nano/count", strawbery_count)
    else:
        client.publish("sys_nano/status", 1)
        print('Stop it')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
    sys.exit()
