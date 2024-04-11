# This script demonstrates how to use pyttsx3 to convert text to speech.

import pyttsx3

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
    engine.setProperty('rate', 150)  # You can adjust the speaking rate (words per minute)
    engine.setProperty('volume', 1)  # You can adjust the volume (0.0 to 1.0)

    # Speak the text
    engine.say(text)

    # Wait for speech to finish
    engine.runAndWait()

# Example usage
text_to_speak = "Hello, how are you?"
speak(text_to_speak)

