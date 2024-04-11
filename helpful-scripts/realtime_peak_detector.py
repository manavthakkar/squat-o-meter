"""
This script demonstrates real-time squat counting using accelerometer data.
It uses the Phyphox app to get the accelerometer data and detects peaks in the data to count squats.

"""

import requests as r
import json
import time
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

url = 'http://192.168.0.103:8080/get?'

def get_accZ(): # Function to get the accelerometer data
    response = r.get(url + '&' + 'accZ').text
    data = json.loads(response)
    # print(data)
    accZ = data['buffer']['accZ']['buffer'][0]
    accZ = float(accZ)
    # print(f'{acc_data:10.7}', end='\n')
    # print()
    return accZ

# Initialize an empty list to store data
data_buffer = []

# Initialize a figure for plotting
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Signal')
peaks_line, = ax.plot([], [], 'x', label='Peaks')
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Real-Time Signal and Peaks')
ax.legend()
ax.grid(True)

# Update function to handle real-time plotting
def update_plot():
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Autoscale
    fig.canvas.flush_events()  # Flush the GUI events
    fig.canvas.draw()  # Redraw the figure

# Main loop for real-time processing
squats_count = 0
buffer_size = 200
data_buffer = []
last_peak_time = time.time()
min_peak_interval = 1.5  # Minimum time interval between peak detections (in seconds)
max_peak_index = 0

while True:
    # Get accelerometer data
    accZ = get_accZ()
    
    # Append data to buffer
    data_buffer.append(accZ)
    
    # Limit buffer size
    if len(data_buffer) > buffer_size:
        data_buffer = data_buffer[-buffer_size:]
    
    # Detect peaks in the accelerometer data
    peaks, _ = find_peaks(data_buffer, height=11.5, distance=10)  # Adjust height threshold as needed

    print("Peak indices:", peaks) # Print the peak indices

    print("Number of peaks:", len(peaks))

    # Check if peaks are detected and ignore subsequent peaks within the threshold
    if len(peaks) > 0:
        current_time = time.time()
        if (peaks[-1] > max_peak_index) and (current_time - last_peak_time > min_peak_interval):
                print("Hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                squats_count += 1
                last_peak_time = current_time
                max_peak_index = peaks[-1]
                print("Squat detected!!!!!!!!!!! Count:", squats_count)
        else:
             max_peak_index = peaks[-1]
    
    # Plot the signal and peaks
    line.set_data(np.arange(len(data_buffer)), data_buffer)
    peaks_line.set_data(peaks, np.array(data_buffer)[peaks])
    
    # Update the plot
    update_plot()

    # Sleep for a short duration to control the loop rate
    time.sleep(0.1)