import datetime
import sys

# Apne khud ke banaye hue modules ko import karna
import config
from voice.speaker import speak
from voice.listener import take_command
from ai.gemini_client import ask_gemini

def wish_me():
    """
    Wishes the user based on the current time of the day.
    """
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Boss!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")
    
    speak(f"{config.ASSISTANT_NAME} is online and ready.")

def start_jarvis():
    """
    The main execution loop for Jarvis.
    """
    # Greeting user on startup
    wish_me()
    
    while True:
        query = take_command()
        
        # Stop commands to turn off Jarvis cleanly
        if "stop" in query or "exit" in query or "bye" in query:
            speak("Goodbye Boss! Have a great day ahead.")
            sys.exit()
            
        if query == "none":
            continue
            
        # Sending query to Gemini and getting response
        response = ask_gemini(query)
        speak(response)

if __name__ == "__main__":
    start_jarvis()