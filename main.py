import pyttsx3

def speak(text):
    """
    Initializes the text-to-speech engine, configures professional 
    voice settings for speed and gender, and outputs the audio.
    """
    # 1. Initialize the speech engine
    engine = pyttsx3.init()
    
    # 2. Configure speaking rate (Speed)
    # Default is usually 200, 170-175 provides a natural human-like pace
    engine.setProperty('rate', 170)
    
    # 3. Configure voice gender/accent
    # Index 0 is typically the default male voice (Microsoft David)
    # Index 1 is typically the default female voice (Microsoft Zira)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) 
    
    # 4. Queue the text and play the audio
    engine.say(text)
    engine.runAndWait()

def main():
    """
    Main entry point for Jarvis AI application.
    """
    print("Voice settings updated. Initializing Jarvis...")
    speak("Hello Boss! Voice settings have been updated. How can I help you today?")

if __name__ == "__main__":
    main()