import speech_recognition as sr

def take_command():
    """
    Listens to the user's microphone and converts speech to text.
    Tries English (India) first, then falls back to Hindi.
    Has timeouts so it never hangs forever waiting on network response.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Koi awaaz nahi aayi, dubara try karo...")
            return "none"

    print("Recognizing...")
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said (English): {query}")
        return query.lower()
    except Exception:
        pass

    try:
        query = r.recognize_google(audio, language='hi-in')
        print(f"User said (Hindi): {query}")
        return query.lower()
    except Exception:
        print("Say that again please...")
        return "none"