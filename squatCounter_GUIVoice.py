"""
This script is a simple GUI application that counts the number of squats performed by the user and provides voice feedback.
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
import pyttsx3


url = 'http://192.168.0.101:8080/get?'

# Parameters for squat detection
buffer_size = 500 # higher buffer size for better accuracy
data_buffer = []
last_peak_time = time.time()
max_peak_index = 0
squats_count = 0
height_threshold = 11.5
distance_threshold = 8
min_peak_interval = 1.0
target_squats = 5

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

def speak(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set a voice (you can experiment with different indices)
    # For example, you can try changing the index to hear different voices
    # The indices vary depending on your system's available voices
    engine.setProperty('voice', voices[1].id)

    # Set properties (optional)
    engine.setProperty('rate', 250)  # You can adjust the speaking rate
    # engine.setProperty('volume', 1)  # You can adjust the volume 

    # Speak the text
    engine.say(text)

    # Wait for speech to finish
    engine.runAndWait()

# Function to detect squats and update the meter
def detect_squats():
    global squats_count
    global data_buffer
    global last_peak_time
    global max_peak_index
    global target_squats
    
    accZ = get_accZ()
    
    data_buffer.append(accZ)
    if len(data_buffer) > buffer_size:
        data_buffer = data_buffer[-buffer_size:]
    
    peaks, _ = find_peaks(data_buffer, height= height_threshold, distance= distance_threshold)  

    if len(peaks) > 0:
        current_time = time.time()
        if (peaks[-1] > max_peak_index) and (current_time - last_peak_time > min_peak_interval):
                squats_count += 1
                speak(str(squats_count))
                # speak(f"Keep it up! You have done {squats_count} squats. {target_squats - squats_count} more to go!")
                # time.sleep(0.2)
                last_peak_time = current_time
                max_peak_index = peaks[-1]
                print("Squat detected! Count:", squats_count)
                # my_meter.step(1) # Increase the meter by 1
                if squats_count < target_squats:
                    my_meter.configure(amountused=squats_count)
                else:
                    my_meter.configure(amountused=target_squats)
                    speak(f"Congratulations! You have reached your target of {target_squats} squats!")
        else:
             max_peak_index = peaks[-1]
             squats_count = int(my_meter.amountusedvar.get()) # Update the squats count from the interactive meter
    
    # Schedule the function to run again after a short delay
    root.after(100, detect_squats)

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
                     amounttotal=target_squats,
                     stepsize=1
                     ) 
my_meter.pack(pady=10, padx=10)

# Start the squat detection function
detect_squats()

root.mainloop()
