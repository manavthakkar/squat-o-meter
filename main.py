"""
This script is a simple GUI application that counts the number of squats performed by the user and provides voice feedback.
The application uses the accelerometer data from the smartphone app to detect squats.
The user can view the number of squats performed on the meter in real-time.
The meter will increase by 1 each time a squat is detected.

"""

from PIL import Image
Image.CUBIC = Image.BICUBIC
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
import time
import requests as r
import json
from scipy.signal import find_peaks
import numpy as np
import pyttsx3
from tkinter.simpledialog import askstring
import ipaddress
import os
from functions import *
import threading
import queue

# Parameters for squat detection
buffer_size = 500 # higher buffer size for better accuracy
data_buffer = []
last_peak_time = time.time()
max_peak_index = 0
squats_count = 0
height_threshold = 11.5
distance_threshold = 8
min_peak_interval = 1.0
target_squats = 10

voice_index = 0
volume = 1

def get_accZ(): 
    try:
        response = r.get(url + '&' + 'accZ').text
        data = json.loads(response)
        
        accZ = data.get('buffer', {}).get('accZ', {}).get('buffer', [None])[0]
        
        if accZ is not None:
            try:
                accZ = float(accZ)
            except ValueError:
                print("Error: Could not convert accZ to float")
                return None
    except r.exceptions.RequestException as e:
        print(f"Error: {e}")
        my_meter.configure(subtext="Connection lost!")
        return None
        
    return accZ

def get_accAbs(): 
    try:
        response = r.get(url + '&' + 'acc').text
        data = json.loads(response)
        
        acc = data.get('buffer', {}).get('acc', {}).get('buffer', [None])[0]
        
        if acc is not None:
            try:
                acc = float(acc)
            except ValueError:
                print("Error: Could not convert acc to float")
                return None
    except r.exceptions.RequestException as e:
        print(f"Error: {e}")
        my_meter.configure(subtext="Connection lost!")
        return None
        
    return acc

def set_target_squats():
    global target_squats
    target_squats = int(target_squats_spinbox.get())
    my_meter.configure(amounttotal=target_squats)
    my_meter.configure(amountused=0)
    # speak(f"Your target number of squats is {target_squats}", voice_index, volume)
    target_squats_button.config(text=f"Target Squats: {target_squats}")

def on_voice_select(event):
    global voice_index
    selected_voice = voice_selector.get()
    # print("Selected voice:", selected_voice)
    voice_index = int(selected_voice.split()[-1]) - 1
    # print("Voice index:", voice_index)

def toggle_volume():
    global volume
    if voice_var.get() == 0:
        volume = 1
        voice_button.config(text="Turn Voice Off")
        print("Value:", voice_var.get())
    else:
        volume = 0
        voice_button.config(text="Turn Voice On")
        print("Value:", voice_var.get())

def toggle_acc():
    if acc_button_var.get() == 1:
        acc_button.config(text="Using Absolute acceleration")
    else:
        acc_button.config(text="Use Absolute acceleration")

def show_acc_threshold(event):
    global height_threshold
    acceleration_threshold_label.config(text=f"Acceleration Threshold: {acceleration_threshold_slider.get():.2f} m/s\u00b2") # Update the label with the current value
    height_threshold = float(acceleration_threshold_slider.get())

def set_buffer_size(event):
    global buffer_size
    buffer_size_label.config(text=f"Moving Window size: {int(buffer_size_slider.get())} samples") # Update the label with the current value
    buffer_size = int(buffer_size_slider.get())

def set_min_peak_interval(event):
    global min_peak_interval
    min_peak_interval_label.config(text=f"Minimum time b/w squats: {min_peak_interval_slider.get():.1f} seconds") # Update the label with the current value
    min_peak_interval = float(min_peak_interval_slider.get())

def save_data():
    if save_button_var.get() == 1:
        # print("Data will be saved to database")
        confirm_save(squats_count)
        save_button_var.set(0)
    # else:
    #     print("Data will not be saved to database")

# Create a queue to hold text to be spoken
speech_queue = queue.Queue()

# Define a function to speak the text
def speak_thread():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()

# Start a new thread to handle speech synthesis
threading.Thread(target=speak_thread, daemon=True).start()

# Modify the speak function to accept the text to be spoken as an argument
def speak(text, voice_index=1, volume=1):
    if volume == 0:
        return
    # Get available voices
    voices = engine.getProperty('voices')

    # Set the desired voice
    engine.setProperty('voice', voices[voice_index].id)

    # Set properties (optional)
    engine.setProperty('rate', 250)  # You can adjust the speaking rate
    engine.setProperty('volume', volume)  # You can adjust the volume 

    # Put the text into the speech queue
    speech_queue.put(text)
def is_valid_ip(address):
    try:
        ipaddress.IPv4Address(address)  # Check if it's a valid IPv4 address
        return True
    except ipaddress.AddressValueError:
        return False

# Function to detect squats and update the meter
def detect_squats():
    global squats_count
    global data_buffer
    global last_peak_time
    global max_peak_index
    global target_squats
    global acc_button_var
    
    if acc_button_var.get() == 1:
        # print("Using absolute acceleration")  
        accZ = get_accAbs()
    else:   
        # print("Using acceleration in Z direction") 
        accZ = get_accZ()

    # If the connection is not refused and the squats count is less than the target squats
    if accZ is not None and squats_count < target_squats:
        my_meter.configure(subtext="Squats done")
    
    data_buffer.append(accZ)
    if len(data_buffer) > buffer_size:
        data_buffer = data_buffer[-buffer_size:]
    
    peaks, _ = find_peaks(data_buffer, height= height_threshold, distance= distance_threshold)  

    if len(peaks) > 0:
        current_time = time.time()
        if (peaks[-1] > max_peak_index) and (current_time - last_peak_time > min_peak_interval):
                squats_count += 1
                # speak(str(squats_count), voice_index, volume)
                last_peak_time = current_time
                max_peak_index = peaks[-1]
                print("Squat detected! Count:", squats_count)
                if squats_count < target_squats:
                    speak(str(squats_count), voice_index, volume)
                    my_meter.configure(amountused=squats_count)
                    # my_meter.configure(subtext="Squats done")
                elif squats_count == target_squats:    
                    my_meter.configure(amountused=target_squats)
                    my_meter.configure(subtext="Target completed!")
                    speak(target_squats, voice_index, volume)
                    speak(f"Congratulations! You have reached your target of {target_squats} squats!", voice_index, volume)
                else:
                    squats_count = 0
                    my_meter.configure(amountused=squats_count)
                    my_meter.configure(subtext="Squats done")
                    target_squats_button.config(text=f"Set Target Squats")
        else:
             max_peak_index = peaks[-1]                         # As the buffer moves, the max_peak_index will change (reduce the index to the last peak detected)
             squats_count = int(my_meter.amountusedvar.get())   # Update the squats count from the interactive meter
    
    # Schedule the function to run again after a short delay
    root.after(100, detect_squats)

root = ttk.Window(themename="superhero")
root.title("Squat-O-Meter")
root.geometry("850x870")

# Set minimum and maximum size of the window
root.minsize(850, 870)
root.maxsize(850, 870)

# Get the path to the script
script_dir = os.path.dirname(__file__)

# Set the icon using a relative path
icon_path = os.path.join(script_dir, "icon.ico")
root.iconbitmap(icon_path)

# Use the queryDialog to prompt the user for input
while True:
    ip_address = askstring('Enter IP Address', 'Please enter the IP address:', parent=root)
    if ip_address is None:
        # User clicked cancel, break out of the loop
        break
    elif is_valid_ip(ip_address):
        print('Entered IP address:', ip_address)
        break  # Break out of the loop if the IP address is valid
    else:
        messagebox.showerror('Error', 'Invalid IP address entered')

url = 'http://' + ip_address + ':8080/get?'

# Create the notebook
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Count Squats')

# create an entry frame to hold widgets above the meter
entry_frame = ttk.Frame(tab1)
entry_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a spinbox widget for the user to enter the target number of squats
target_squats_spinbox = ttk.Spinbox(entry_frame, from_=0, to=500, 
                                    bootstyle="success", 
                                    font=("Helvetica", 14), 
                                    state="readonly", width=8)
target_squats_spinbox.grid(row=0, column=1, padx=10, pady=20)

# Set the default value of the spinbox to 5
target_squats_spinbox.set(10)

# Create a button to set the target number of squats
target_squats_button = ttk.Button(entry_frame, text="Set Target Squats", command=set_target_squats)
target_squats_button.grid(row=1, column=1, padx=20)

# Create buffer size slider
buffer_size_slider = ttk.Scale(entry_frame, 
                                          from_=100, 
                                          to=500, 
                                          length=240, 
                                          orient="horizontal", 
                                          bootstyle="success",
                                          command=set_buffer_size)

buffer_size_slider.grid(row=0, column=0, padx=20)

# Create a label to display the buffer size value
buffer_size_label = ttk.Label(entry_frame, text="", font=("Helvetica", 10))
buffer_size_label.grid(row=1, column=0, padx=20)

# Set the default value of the buffer size slider
buffer_size_slider.set(500)

# Create minimum peak interval slider
min_peak_interval_slider = ttk.Scale(entry_frame,
                                            from_=0.5, 
                                            to=2, 
                                            length=240, 
                                            orient="horizontal", 
                                            bootstyle="success",
                                            command=set_min_peak_interval)

min_peak_interval_slider.grid(row=0, column=2, padx=20)

# Create a label to display the minimum peak interval value
min_peak_interval_label = ttk.Label(entry_frame, text="", font=("Helvetica", 10))
min_peak_interval_label.grid(row=1, column=2, padx=20)

# Set the default value of the minimum peak interval slider
min_peak_interval_slider.set(1.0)

# create a frame to hold the widgets in meter region
meter_frame = ttk.Frame(tab1)
meter_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create an empty label on the left side of the meter
empty_label = ttk.Label(meter_frame, text="", font=("Helvetica", 10))
empty_label.grid(row=0, column=0, padx=55)


# Create a meter widget to display the number of squats performed
my_meter = ttk.Meter(meter_frame, bootstyle="danger", 
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
my_meter.grid(row=0, column=1, padx=20)

# create a frame to hold the widgets below the meter
parameters_frame = ttk.Frame(tab1)
parameters_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Get the number of voices available in the system
no_of_voices = len(pyttsx3.init().getProperty('voices'))

# List of voices available in the system
voice_list = ['Voice {}'.format(i) for i in range(1, no_of_voices + 1)] # Create a list of voice names -> ['Voice 1', 'Voice 2', 'Voice 3', ...]

# Create a combobox widget to select the voice (dropdown menu)
voice_selector = ttk.Combobox(parameters_frame, bootstyle="success", values = voice_list, state="readonly", font=("Helvetica", 10), width=10)
voice_selector.grid(row=0, column=0, padx=20, pady=10)

# Set the default value of the combobox to the last item in the list
voice_selector.set(voice_list[0]) # Set the default voice to the first voice in the list

# Bind the event to the combobox
voice_selector.bind("<<ComboboxSelected>>", on_voice_select)

# Create a toolbutton to turn on/off the voice feedback
voice_var = IntVar()
voice_button = ttk.Checkbutton(parameters_frame, 
                               text="Turn Voice Off", 
                               variable=voice_var,
                               command=toggle_volume,
                               onvalue=1, offvalue=0,
                               bootstyle="success, toolbutton",
                               width=12)
voice_button.grid(row=1, column=0, padx=20, pady=10)

# Style the round toggle button for acceleration
acc_style = ttk.Style()
acc_style.configure("success.TCheckbutton", font=("Helvetica", 12))

# Round toggle button to toggle between absolute acceleration and acceleration in Z direction
acc_button_var = IntVar()
acc_button = ttk.Checkbutton(parameters_frame,
                             bootstyle="success, round-toggle", # it doesn't appear round in the GUI as the style is overriding it
                             text="Use Absolute Acceleration",
                             variable=acc_button_var,
                             onvalue=1, 
                             offvalue=0,
                             command=toggle_acc,
                             style="success.TCheckbutton"
                             )
acc_button.grid(row=0, column=1, padx=25, pady=10)

# Create a check button to ask user to save the data to database
save_button_var = IntVar()
save_button = ttk.Checkbutton(  parameters_frame,
                                bootstyle="success, toolbutton, outline",
                                text="Save to Database",
                                variable=save_button_var,
                                width=22,
                                onvalue=1,
                                offvalue=0,
                                command=save_data)
save_button.grid(row=1, column=1, padx=15, pady=10)

# Create a label to display the acceleration threshold value
acceleration_threshold_label = ttk.Label(parameters_frame, text="", font=("Helvetica", 10))
acceleration_threshold_label.grid(row=1, column=2, padx=20)

# Create a slider widget to adjust the acceleration threshold
acceleration_threshold_slider = ttk.Scale(parameters_frame, 
                                          from_=10, 
                                          to=15, 
                                          length=240, 
                                          orient="horizontal", 
                                          bootstyle="success",
                                          command=show_acc_threshold)

acceleration_threshold_slider.grid(row=0, column=2, padx=20)

# Set the default value of the slider
acceleration_threshold_slider.set(11.5)

# Create tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Analyze Data')

# Add a button to tab 2
button = ttk.Button(tab2, text="Button")
button.pack(pady=20)

# Initialize the pyttsx3 engine outside the speak function
engine = pyttsx3.init()

# Start the squat detection function
detect_squats()

# Call engine.runAndWait() before the main event loop to ensure any pending speech is spoken
engine.runAndWait()

root.mainloop()
