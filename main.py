import os
import sys
import datetime
import speech_recognition as sr

def speak(text):
    """
    Outputs the string text by invoking the native Windows PowerShell 
    Speech Synthesis engine directly to bypass registry locks.
    """
    print(f"Jarvis: {text}")
    # Sanitizing string quotation marks for PowerShell execution safety
    clean_text = text.replace("'", "").replace('"', "")
    powershell_command = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
    os.system(powershell_command)

def take_command():
    """
    Listens to microphone input from the user and returns the 
    recognized text as a clean lowercase string output.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return str(query).lower().strip()
        
    except sr.UnknownValueError:
        print("System Warning: Audio unrecognized.")
        return "none"
    except sr.RequestError:
        print("System Error: API network request failed.")
        return "none"

def main():
    """
    Main execution lifecycle loop for the Jarvis assistant framework.
    """
    print("Native OS sound routing initialized successfully.")
    speak("Jarvis is online. Core automated modules initialized, Boss.")
    
    while True:
        user_input = take_command()
        
        if user_input == "none":
            continue
            
        if "exit" in user_input or "stop" in user_input or "quit" in user_input:
            speak("Understood, Boss. Shutting down systems. Goodbye.")
            sys.exit()
            
        if "hello" in user_input:
            speak("Hello Boss! Core systems are monitoring your workspace.")
            
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}, Boss.")
            
        elif "notepad" in user_input:
            speak("Opening Notepad text editor, Boss.")
            os.system("notepad.exe")
            
        elif "chrome" in user_input:
            speak("Launching Google Chrome browser, Boss.")
            os.system("start chrome")
            
        else:
            speak(f"Processing backup logic sequence. You said: {user_input}")

if __name__ == "__main__":
    main()