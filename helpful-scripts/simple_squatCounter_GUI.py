"""
This script is a simple GUI application that counts the number of squats performed by the user. 
The application uses the accelerometer data from the smartphone app to detect squats. 
The user can view the number of squats performed on the meter in real-time. 
The meter will increase by 1 each time a squat is detected. 

"""

from PIL import Image
Image.CUBIC = Image.BICUBIC
from tkinter import *
import ttkbootstrap as ttk
import time
import requests as r
import json
from scipy.signal import find_peaks
import numpy as np


url = 'http://192.168.0.101:8080/get?'

def get_accZ(): 
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

# Function to detect squats and update the meter
def detect_squats():
    global squats_count
    global data_buffer
    global last_peak_time
    global max_peak_index
    
    accZ = get_accZ()
    
    data_buffer.append(accZ)
    if len(data_buffer) > buffer_size:
        data_buffer = data_buffer[-buffer_size:]
    
    peaks, _ = find_peaks(data_buffer, height= height_threshold, distance= distance_threshold)  

    if len(peaks) > 0:
        current_time = time.time()
        if (peaks[-1] > max_peak_index) and (current_time - last_peak_time > min_peak_interval):
                squats_count += 1
                # time.sleep(0.2)
                last_peak_time = current_time
                max_peak_index = peaks[-1]
                print("Squat detected! Count:", squats_count)
                # my_meter.step(1) # Increase the meter by 1
                my_meter.configure(amountused=squats_count)
        else:
             max_peak_index = peaks[-1]
    
    # Schedule the function to run again after a short delay
    root.after(100, detect_squats)

buffer_size = 250 # higher buffer size for better accuracy
data_buffer = []
last_peak_time = time.time()
max_peak_index = 0
squats_count = 0
height_threshold = 11.5
distance_threshold = 8
min_peak_interval = 1

root = ttk.Window(themename="superhero")
root.title("Squat-O-Meter")
root.geometry("600x600")

my_meter = ttk.Meter(root, bootstyle="danger", 
                     textfont=("Helvetica", 50),
                     subtext="Squats done ",
                     subtextstyle="light",
                     subtextfont=("Helvetica", 20),
                     interactive=True,
                     textright="",
                     metertype="full", # or "full" or "semi"
                     stripethickness=10,
                     metersize=400,
                     padding=10,
                     amountused=0,
                     amounttotal=10,
                     stepsize=1
                     ) 
my_meter.pack(pady=10, padx=10)

# Start the squat detection function
detect_squats()

root.mainloop()
