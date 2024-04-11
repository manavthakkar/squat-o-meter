"""
This is a script that plots the real-time data from the accelerometer sensor in the Z-axis.
The data is fetched from the Phyphox app using the requests library.
The data is then plotted using the matplotlib library.

"""

import requests as r
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

url = 'http://192.168.1.103:8080/get?'
what_to_get = ['accZ']

# List to store the accZ data
accZ_data = []

def phyphox_data():
    response = r.get(url + '&'.join(what_to_get)).text
    data = json.loads(response)
    acc_data = data['buffer']['accZ']['buffer'][0]  # Directly use 'accZ' instead of item
    accZ_data.append(acc_data)  # Add the new data to the list
    return accZ_data

# Function to update the plot
def update(frame):
    accZ_data = phyphox_data()
    line.set_ydata(accZ_data)
    line.set_xdata(range(len(accZ_data)))
    ax.relim()
    ax.autoscale_view()
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Set up the plot for animation
ani = FuncAnimation(fig, update, blit=True, save_count=100)

plt.show()