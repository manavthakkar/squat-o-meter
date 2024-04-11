"""
This script reads the magnetometer data from the Phyphox app and prints it to the console.
The data is collected from the Phyphox app, which records magnetometer data from a smartphone's magnetometer.
The data obtained can be used for further analysis or visualization.

"""

import requests as r
import json
import time

url = 'http://192.168.1.103:8080/get?'
what_to_get = ['magX', 'magY', 'magZ', 'mag']


def phyphox_data():
    response = r.get(url + '&'.join(what_to_get)).text
    data = json. loads(response)
    for item in what_to_get:
        mag_data = data['buffer'][item]['buffer'][0]
        print(f'{mag_data:10.7}', end='\t')
    print()

while True:
    phyphox_data()
    time.sleep(0.1)