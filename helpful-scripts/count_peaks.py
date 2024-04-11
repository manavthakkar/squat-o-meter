"""
This script demonstrates how to count the number of peaks in a signal using the `find_peaks` function from the `scipy.signal` module.
The script reads a CSV file containing acceleration data and identifies the peaks in the signal.
The CSV file is generated from the Phyphox app, which records acceleration data from a smartphone's accelerometer.
"""

import pandas as pd
import pylab as plt
import numpy as np
from scipy.signal import find_peaks
 
df = pd.read_csv('4_squats.csv')

# Define the new column names
new_column_names = {
    'Time (s)': 't',
    'Acceleration x (m/s^2)': 'x',
    'Acceleration y (m/s^2)': 'y',
    'Acceleration z (m/s^2)': 'z',
    'Absolute acceleration (m/s^2)': 'abs'
}

# Rename the columns
df = df.rename(columns=new_column_names)

# Find peaks in the "z" column of the DataFrame (the acceleration data along the z-axis)
peaks, _ = find_peaks(df['z'], height=12.0, distance=1000) 

# Plot the signal and the identified peaks
plt.plot(df.index, df['z'])
plt.plot(df.index[peaks], df['z'][peaks], "x")
plt.xlabel('Index')
plt.ylabel('Amplitude')
plt.title('Signal with Peaks')
plt.show()

# `peaks` contains the indices of the peaks in the signal (the time points where the signal reaches its maximum value)
print("Peak indices:", peaks)

# print type of peaks 
# print(type(peaks))     # <class 'numpy.ndarray'>

# To get the peak values, you can simply index the signal with the peak indices (value of acceleration at the time points where the peaks occur)
# print("Peak values:", df['z'][peaks]) 

# print side by side the index and the value of the peaks
for i in range(len(peaks)):
    print("Index:", peaks[i], "Value:", df['z'][peaks[i]])

# The number of peaks can be obtained by checking the length of the `peaks` array
print("Number of peaks:", len(peaks))
