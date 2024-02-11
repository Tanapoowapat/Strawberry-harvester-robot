import paho.mqtt.client as mqtt
from image_processing import start_process


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rasp/v_s")

def on_message(client, userdata, msg):

    received_data = msg.payload
    decoded_data = received_data.decode('utf-8')

    # print(msg.topic+" = "+str(msg.payload))
    print(msg.topic+" = "+decoded_data)
    
    if decoded_data == '1':
        start_process()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()