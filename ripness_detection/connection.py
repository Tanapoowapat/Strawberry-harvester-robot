import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rasp/v_s")

def on_message(client, userdata, msg):

    received_data = msg.payload
    decoded_data = received_data.decode('utf-8')

    # print(msg.topic+" = "+str(msg.payload))
    print(msg.topic+" = "+decoded_data)
    # print(type(msg.payload))

    # if decoded_data == '10' or decoded_data.isdigit(): 
    #print(f'Server sand : {decoded_data}')
    print(f'Server staby')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.137.41", 1883, 60)

client.loop_forever()