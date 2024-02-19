import paho.mqtt.client as mqtt
import time
import json
import threading
import sys
from image_processing import start_process

def on_connect(client, userdata, flags, rc):
    client.subscribe("rasp/v_s")
    if rc == 0:
        client.publish("pi/status", 1)
        print("======================\nConnected successfully\n======================")
    else:
        client.publish("pi/status", 3)
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    received_data = msg.payload
    json_data = json.loads(received_data)
    global ch  
    #print(f'Server sand : {json_data} Type: {type(json_data)}\n')
    #ch = json_data['ripeness']
    ch = 'qwe'
    #print(f'Server sand : {ch} Type : {type(ch)}\n')

    client.publish("js/outp", json_data['ripeness'])
    if ch == 'q' :
        client.publish("pi/status", 3)
        print('Received "q". Stopping the program.')
        client.disconnect()
        sys.exit()
    if 'ripeness' in json_data:
        ripeness_level = None
        ripeness = json_data['ripeness']
        if ripeness == 1:
            ripeness_level = 'Unripe' 
        elif ripeness == 2:
            ripeness_level = 'SmallRipe' 
        elif ripeness == 3:
            ripeness_level = 'MediumRipe' 
        elif ripeness == 4:
            ripeness_level = 'Ripe' 
        elif ripeness == 5:
            ripeness_level = 'FullRipe' 
        else:
            print('unknow input')

        if ripeness_level is not None:
            start_process(ripeness_level)

        #threading.Thread(target=gpio_loop_and_sleep).start()
    else :
        client.publish("pi/status", 1)
        print('Stop it')
    # onlime_sta()
   # print('====================\nServer Status Stanby\n====================')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
# client.loop_forever()

client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
    sys.exit()