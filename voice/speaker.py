from gtts import gTTS
from playsound import playsound
import os
import uuid

def speak(text):
    """
    Converts text to natural speech using Google's TTS engine (gTTS).
    Works well across Hindi, English, and Hinglish text since it uses
    the Hindi voice model, which handles mixed-language content smoothly.
    Requires an active internet connection.
    """
    print(f"Jarvis: {text}")

    filename = f"jarvis_voice_{uuid.uuid4().hex}.mp3"
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(filename)
        playsound(filename)
    except Exception as e:
        print(f"[SPEAKER ERROR]: {e}")
    finally:
        # Temporary audio file ko clean up karna taaki folder mein kachra na jama ho
        if os.path.exists(filename):
            os.remove(filename)