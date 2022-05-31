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
import pprint
from collections import defaultdict
val= {
  "t": 1625576100,
  "r": [
    {
      "_d": "logger",
      "_vid": "strato-1",
      "boot_time": 1625563315,
      "cpu_load": 0.06,
      "memory_usage": 17.2
    },
    {
      "_d": "logger_strato",
      "_vid": "strato-1",
      "cpu_temp": 60.148,
      "disk_usage": 45.8
    },
    {
      "_d": "diesel_sensor",
      "_vid": "gamicos-1",
      "analog": 5.814655303955078,
      "level": 0.5670797228813171,
      "genset_fuel_level_percent": 56.378482855283295,
      "genset_fuel_volume": 2477.2705366611485
    },
    {
      "_d": "dse855",
      "_vid": "dse-1",
      "E": 86744200,
      "P": 15983,
      "P_L1": 4823,
      "P_L2": 4720,
      "P_L3": 6440,
      "S": 17293,
      "S_L1": 5314,
      "S_L2": 5109,
      "S_L3": 6901,
      "V_L1": 229.5,
      "V_L2": 231,
      "V_L3": 229.70000000000002,
      "alarm_status": 0,
      "freq": 50,
      "oil_pressure": 406,
      "power_factor": 0.92,
      "power_factor_L1": 0.9,
      "power_factor_L2": 0.92,
      "power_factor_L3": 0.93,
      "runtime": 14316904,
      "temp_coolant": 78,
    }
  ],
  "m": {
    "snap_rev": 670,
    "config_id": "c5b2543",
    "reading_duration": 0.9248790740966797,
    "reading_offset": 0
  }
}

val['t'] = datetime.datetime.fromtimestamp(val['t']).isoformat()
val['time'] = val.pop('t')
val['data'] = val.pop('r')
del val['m']
res = map(lambda dict_tuple: dict(ChainMap(*dict_tuple[1])),
          groupby(sorted(val['data'],
                         key=lambda sub_dict: sub_dict["_vid"]),
                  key=lambda sub_dict: sub_dict["_vid"]))
del val['data']
val['data'] = list(res)
final = defaultdict(dict)
for k, v in val.items():
    if 'data' in k:
        for index in range(len(val['data'])):

            if len(val['data'][index]) > 2:
              newKey = val['data'][index]['_vid']
              del val['data'][index]['_d']
              del val['data'][index]['_vid']
              for cleanKey,value in val['data'][index].items():
                final[newKey][cleanKey] = value

del val['data']
final = dict(final)
val['data'] = final


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


pprint.pprint(clean_nones(val))