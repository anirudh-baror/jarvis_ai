import os
import sys
import datetime
import speech_recognition as sr
from google import genai

# Initialize Gemini Client
# TODO: Apni copy ki hui API key yahan single quotes ke andar paste kijiye
client = genai.Client(api_key='YOUR_GEMINI_API_KEY_HERE')

def speak(text):
    """
    Outputs the string text by invoking the native Windows PowerShell 
    Speech Synthesis engine directly.
    """
    print(f"Jarvis: {text}")
    clean_text = text.replace("'", "").replace('"', "")
    powershell_command = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
    os.system(powershell_command)

def ask_gemini(question):
    """
    Sends the user query to Google Gemini LLM and returns a concise text response.
    """
    try:
        print("Thinking...")
        prompt = f"You are Jarvis, a witty and highly intelligent AI assistant. Answer this question concisely in 2-3 sentences max: {question}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sorry Boss, network network issue."

def take_command():
    """
    Listens to microphone input and converts it to text with aggressive timeouts to prevent lag.
    """
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True  # Aas-paas ke shor ko automatically handle karega
    recognizer.pause_threshold = 0.8  # Bolne ke baad sirf 0.8 second ka wait karega aur process shuru

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            # timeout=3 (3 sec tak kuch nahi bole toh skip), phrase_time_limit=4 (max 4 sec ki recording)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)

        print("Recognizing...")
        # Google Speech Recognition online API
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return str(query).lower().strip()
        
    except Exception:
        # Kuch bhi error aaye (timeout, blank audio, network lag), seedha bina atke aage badho
        return "none"

def main():
    """
    Main execution lifecycle loop for the Jarvis Voice Assistant.
    """
    print("Native OS sound routing initialized successfully.")
    speak("Jarvis Voice System online, Boss.")
    
    while True:
        user_input = take_command()
        
        if user_input == "none" or user_input == "":
            continue
            
        if "exit" in user_input or "stop" in user_input or "quit" in user_input:
            speak("Understood, Boss. Shutting down systems. Goodbye.")
            sys.exit()
            
        # PC Automation Commands
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}, Boss.")
            
        elif "notepad" in user_input:
            speak("Opening Notepad text editor, Boss.")
            os.system("notepad.exe")
            
        elif "chrome" in user_input:
            speak("Launching Google Chrome browser, Boss.")
            os.system("start chrome")
            
        # AI Intelligence Layer
        else:
            ai_response = ask_gemini(user_input)
            speak(ai_response)

if __name__ == "__main__":
    main()