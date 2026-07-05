import datetime
import sys

# Importing custom project configuration and core modules
import config
from voice.speaker import speak
from voice.listener import take_command
from ai.gemini_client import ask_gemini

# Importing web automation functions from the automation package
from automation.browser import open_youtube, play_on_youtube, search_google

def wish_me():
    """Wishes the user based on the current time of the day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Boss!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")
    
    speak(f"{config.ASSISTANT_NAME} is online and ready.")

def start_jarvis():
    """The main execution loop for Jarvis."""
    wish_me()
    
    while True:
        # Listen for user voice command
        query = take_command()
        
        # Termination clauses to safely stop the assistant
        if "stop" in query or "exit" in query or "bye" in query:
            speak("Goodbye Boss! Have a great day ahead.")
            sys.exit()
            
        if query == "none":
            continue
            
        # Browser and Web Automation routing
        if "open youtube" in query:
            speak("Opening YouTube, Boss.")
            open_youtube()
            continue
            
        elif "play" in query and "youtube" in query:
            # Example: "play coding lofi on youtube" -> extracts "coding lofi"
            song = query.replace("play", "").replace("on youtube", "").strip()
            speak(f"Playing {song} on YouTube, Boss.")
            play_on_youtube(song)
            continue
            
        elif "search" in query or "google" in query:
            # Example: "search space exploration news" -> extracts search query
            search_item = query.replace("search", "").replace("google", "").strip()
            speak(f"Searching Google for {search_item}, Boss.")
            search_google(search_item)
            continue

        # Default fallback: Route conversational queries to Gemini AI
        response = ask_gemini(query)
        speak(response)

if __name__ == "__main__":
    start_jarvis()