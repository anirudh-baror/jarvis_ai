from google import genai
from dotenv import load_dotenv
import os
import config

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY

client = genai.Client(api_key=API_KEY)

def ask_gemini(question):
    """
    Sends the user query to Google Gemini LLM and returns a concise,
    bilingual (Hindi + English) text response — matches user's language.
    Hindi responses are in Roman script so both terminal display and
    TTS voice work correctly.
    """
    try:
        prompt = (
            "You are Jarvis, a witty and highly intelligent AI assistant with broad "
            "general knowledge on any topic that exists in the world. "
            "Always reply in the SAME language the user used — "
            "agar user Hindi mein poochta hai toh Hindi mein hi jawab do LEKIN Roman/English letters mein likho "
            "(Devanagari script mat use karo), jaise 'Bharat ki rajdhani Nai Dilli hai', "
            "agar English mein poochta hai toh English mein do, "
            "aur agar Hinglish mein poochta hai toh usi Hinglish style mein jawab do. "
            "Never refuse a general-knowledge question — answer confidently. "
            f"Answer this concisely in 2-3 sentences max: {question}"
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"\n[GEMINI ERROR]: {e}\n")
        return "Sorry Boss, network network issue."