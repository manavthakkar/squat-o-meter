"""
This is a simple example of how to use the Meter widget.
The Meter widget is a circular progress bar that can be used to display the progress of a task.
It can be used to display the progress of a task in a graphical way.

"""

from PIL import Image
Image.CUBIC = Image.BICUBIC
from tkinter import *
import ttkbootstrap as ttk
import time

root = ttk.Window(themename="superhero")

root.title("Meter Widgets")
root.geometry("600x600")

my_meter = ttk.Meter(root, bootstyle="danger", 
                     textfont=("Helvetica", 50),
                     subtext="Squats done ",
                     subtextstyle="light",
                     subtextfont=("Helvetica", 20),
                     interactive=True,
                     textright="$",
                     metertype="full", # or "full" or "semi"
                     stripethickness=10,
                     metersize=400,
                     padding=10,
                     amountused=0,
                     amounttotal=10,
                     stepsize=1
                     ) 
my_meter.pack(pady=10, padx=10)


my_meter.step(1) # Increase the meter by 1


root.mainloop()
