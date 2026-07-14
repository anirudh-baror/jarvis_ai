import datetime
import sys

# Core configuration and voice sub-modules
import config
from ai.memory import init_db
from voice.speaker import speak
from voice.listener import take_command
from ai.gemini_client import ask_gemini

# Web automation module capabilities
from automation.browser import open_youtube, play_on_youtube, search_google

def wish_me():
    """Greets the user dynamically based on the system time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Boss!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")
    
    speak(f"{config.ASSISTANT_NAME} is online and fully operational.")

def start_jarvis():
    """Main execution thread mapping speech intents to actions or AI logic."""
    init_db()
    wish_me()
    
    while True:
        query = take_command()
        
        # Immediate termination signals
        if "stop" in query or "exit" in query or "bye" in query:
            speak("Goodbye Boss! Systems shutting down cleanly.")
            sys.exit()
            
        # Ignore empty audio responses
        if query == "none":
            continue
            
        # Intent Routing: Web Browsing Automation
        if "open youtube" in query:
            speak("Opening YouTube right away, Boss.")
            open_youtube()
            continue
            
        elif "play" in query and "youtube" in query:
            # Isolates the song name from the spoken query phrase
            song = query.replace("play", "").replace("on youtube", "").strip()
            speak(f"Searching and playing {song} on YouTube, Boss.")
            play_on_youtube(song)
            continue
            
        elif "search" in query or "google" in query:
            # Isolates the target search phrase
            search_item = query.replace("search", "").replace("google", "").strip()
            speak(f"Searching Google index for {search_item}, Boss.")
            search_google(search_item)
            continue

        # Intent Routing: Fallback directly to generative AI capabilities
        response = ask_gemini(query)
        speak(response)

if __name__ == "__main__":
    start_jarvis()