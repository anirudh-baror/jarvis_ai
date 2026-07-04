import speech_recognition as sr

def take_command():
    """
    Listens to the user's microphone and converts speech to text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return "None"