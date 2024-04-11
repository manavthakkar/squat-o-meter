"""
This is a script that uses the Phyphox app to get the acceleration data and plots it in real-time.

"""

import requests as r
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks

url = 'http://192.168.0.103:8080/get?'
what_to_get = ['accZ']

# List to store the accZ data
accZ_data = []

def phyphox_data():
    response = r.get(url + '&'.join(what_to_get)).text
    data = json.loads(response)
    acc_data = data['buffer']['accZ']['buffer'][0]  #
    accZ_data.append(acc_data)  # Add the new data to the list
    return accZ_data

# Function to update the plot
def update(frame):
    accZ_data = phyphox_data()
    peaks, _ = find_peaks(accZ_data, height=12.0, distance=1000)  # Find the peaks
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