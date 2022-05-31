from paho.mqtt import client as mqtt_client
from time import sleep
import json
import os
broker = 'mqtt.stage.ammp.io'
port = 8883
topic = "a/b827eb391de9/data"
username = 'ammp_challenge'
password = '6Z7BzbaPPrwL6p'



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

    client.subscribe("a/b827eb391de9/data")

# Set Connecting Client ID
client = mqtt_client.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()

def on_message(client, userdata, message):
    val = json.loads(message.payload)
    print(val)
    client.loop_stop()
    client.disconnect()
    os._exit(0)

while True:
    sleep(1)

