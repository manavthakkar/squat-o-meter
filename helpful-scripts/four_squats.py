"""
This script reads the data from the 4_squats.csv file and plots the x, y, and z acceleration values on the same graph.
The data is collected from the Phyphox app, which records acceleration data from a smartphone's accelerometer.
This script helps visualize the acceleration values over time.

"""

import pandas as pd
import pylab as plt
 
df = pd.read_csv('4_squats.csv')

# Print the column names
# print(df.columns)

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
 
print(df.head())

# plot the x,y,z acceleration values on the same graph
plt.figure(figsize=(8, 8))
plt.plot(df['t'], df['x'], label='x')
plt.plot(df['t'], df['y'], label='y')
plt.plot(df['t'], df['z'], label='z')
plt.legend()
plt.title('Acceleration values')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.show()
