import datetime
import sys

# Core configuration and voice sub-modules
import config
from ai.memory import init_db
from voice.speaker import speak
from voice.listener import take_command
from ai.gemini_client import ask_gemini

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
    """Main execution thread. Routes user speech to Gemini, which decides
    whether to answer directly or call a browser automation tool."""
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

        # Everything else goes to Gemini — it decides whether to answer
        # directly or call a tool (YouTube, Google search, etc.)
        response = ask_gemini(query)
        speak(response)

if __name__ == "__main__":
    start_jarvis()