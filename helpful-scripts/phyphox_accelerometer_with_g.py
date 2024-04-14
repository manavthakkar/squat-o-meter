"""
This script reads the accelerometer data from Phyphox and prints it to the console.
The data is collected from the Phyphox app, which records acceleration data from a smartphone's accelerometer.
The data obtained then later can be used for further analysis or visualization.

"""

import requests as r
import json
import time

url = 'http://192.168.0.101:8080/get?'

what_to_get = ['accX', 'accY', 'accZ', 'acc']

def phyphox_data():
    try:
        response = r.get(url + '&'.join(what_to_get))
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        for item in what_to_get:
            acc_data = data['buffer'][item]['buffer'][0]
            print(f'{acc_data:10.7}', end='\t')
        print()
    except r.exceptions.RequestException as e:
        print(f"Error: {e}")
        # You can add additional error handling or logging here if needed

while True:
    phyphox_data()
    time.sleep(0.1)
