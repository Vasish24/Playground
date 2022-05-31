import datetime
import time
from time import sleep
import ssl
import json
import os
from paho.mqtt.client import Client
from itertools import groupby
from pprint import pprint
from collections import ChainMap
from collections import defaultdict

broker = 'mqtt.stage.ammp.io'
port = 8883
topic = "a/b827eb391de9/data"
username = 'ammp_challenge'
password = '6Z7BzbaPPrwL6p'

def on_message(client, userdata, message):
    """
    The raw data is received and cleaned in this function

    """
    val = json.loads(message.payload)                                   #Payload is received
    val['t'] = datetime.datetime.fromtimestamp(val['t']).isoformat()    #Timestamp conversion
    val['time'] = val.pop('t')
    val['data'] = val.pop('r')
    del val['m']                                                        #Discarding the remaining metadata
    res = map(lambda dict_tuple: dict(ChainMap(*dict_tuple[1])),        #Grouping the data,according to the vendor_id
              groupby(sorted(val['data'],
                             key=lambda sub_dict: sub_dict["_vid"]),
                      key=lambda sub_dict: sub_dict["_vid"]))
    del val['data']
    val['data'] = list(res)
    final_data = defaultdict(dict)
    for k, v in val.items():
        if 'data' in k:
            for index in range(len(val['data'])):                       #Field with _d and _vid has been discraded
                if len(val['data'][index]) > 2:
                    newKey = val['data'][index]['_vid']
                    del val['data'][index]['_d']
                    del val['data'][index]['_vid']
                    for cleanKey, value in val['data'][index].items():
                        final_data[newKey][cleanKey] = value

    del val['data']
    final_data = dict(final_data)
    val['data'] = final_data
    #print(val)
    pprint(clean_nones(val))
    client.loop_stop()
    client.disconnect()
    os._exit(0)


def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value

def on_connect(client, userdata, rc, *args):
    client.subscribe("a/b827eb391de9/data")                              #Subscribe the topic


client = Client()
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.username_pw_set(username, password)
client.connect(broker, port, keepalive=60)                                             #Connect to broker
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while True:
    sleep(1)                                                             #wait
