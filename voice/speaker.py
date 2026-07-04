import os

def speak(text):
    """
    Outputs the string text by invoking the native Windows PowerShell
    Speech Synthesis engine directly.
    """
    print(f"Jarvis: {text}")
    
    # Text ko saaf karna taaki PowerShell quotes se confuse na ho
    clean_text = text.replace("'", "").replace('"', "")
    
    # Native Windows TTS Voice Command
    powershell_command = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
    
    # Command ko run karna
    os.system(powershell_command)