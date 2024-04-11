'''
This script is used to count the number of squats performed in real-time using the accelerometer data from the smartphone.
The script reads the accelerometer data from the Phyphox app running on the smartphone and detects peaks in the Z-axis
acceleration data to identify squat movements. The number of squats performed is displayed in the console and the real-time
accelerometer data and detected peaks are plotted on a graph.

Change the URL to match the IP address of the smartphone running the Phyphox app.
Instead of using the Z-axis acceleration data, you can also use the absolute acceleration data by changing the function to get_accAbs().
In that case it might detect more peaks as it is not dependent on the orientation of the phone.

'''

import requests as r
import json
import time
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

url = 'http://192.168.0.103:8080/get?'

def get_accZ(): 
    '''
    Function to get the accelerometer data

    Returns:
    accZ: float, accelerometer data in the Z-axis
    
    '''
    response = r.get(url + '&' + 'accZ').text
    data = json.loads(response)
    
    accZ = data.get('buffer', {}).get('accZ', {}).get('buffer', [None])[0]
    
    if accZ is not None:
        try:
            accZ = float(accZ)
        except ValueError:
            print("Error: Could not convert accZ to float")
            return None
        
    return accZ


def get_accAbs(): 
    '''
    Function to get the accelerometer data

    Returns:
    accZ: float, accelerometer data (absolute value)
    
    '''
    response = r.get(url + '&' + 'acc').text
    data = json.loads(response)
    
    acc = data.get('buffer', {}).get('acc', {}).get('buffer', [None])[0]
    
    if acc is not None:
        try:
            acc = float(acc)
        except ValueError:
            print("Error: Could not convert accZ to float")
            return None
        
    return acc


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
    ax.relim()                  # Recalculate limits
    ax.autoscale_view()         # Autoscale
    fig.canvas.flush_events()   # Flush the GUI events
    fig.canvas.draw()           # Redraw the figure

# Main loop for real-time processing
squats_count = 0
buffer_size = 200               # Buffer size for storing accelerometer data (sliding window sample size)
data_buffer = []                # Initialize an empty list to store the accelerometer data
last_peak_time = time.time()    # Initialize the time of the last peak detection
max_peak_index = 0              # Initialize the index of the last peak detected

# Parameters for peak detection (adjust as needed)
height_threshold = 11.5         # Threshold for peak detection (in m/s^2)
distance_threshold = 10         # Minimum distance between peaks (in samples)
min_peak_interval = 1.5         # Minimum time interval between peak detections (in seconds)

while True:
    # Get accelerometer data from the Z-axis
    accZ = get_accZ()
    
    # Append data to buffer
    data_buffer.append(accZ)
    
    # Limit buffer size 
    if len(data_buffer) > buffer_size:
        data_buffer = data_buffer[-buffer_size:]
    
    # Detect peaks in the accelerometer data
    peaks, _ = find_peaks(data_buffer, height= height_threshold, distance= distance_threshold)  

    # Check if peaks are detected and ignore subsequent peaks within the threshold
    if len(peaks) > 0:
        current_time = time.time()
        if (peaks[-1] > max_peak_index) and (current_time - last_peak_time > min_peak_interval):
                squats_count += 1
                last_peak_time = current_time
                max_peak_index = peaks[-1]
                print("Squat detected! Count:", squats_count)
        else:
             max_peak_index = peaks[-1]
    
    # Plot the signal and peaks
    line.set_data(np.arange(len(data_buffer)), data_buffer)
    peaks_line.set_data(peaks, np.array(data_buffer)[peaks])
    
    # Update the plot
    update_plot()

    # Sleep for a short duration to control the loop rate
    time.sleep(0.1)