from google import genai
from dotenv import load_dotenv
import os
import config

# .env file se variables ko system environment mein load karna
load_dotenv()

# Sabse pehle .env se key uthane ki koshish karenge, agar wahan nahi mili toh config.py se lenge
API_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY

# Gemini Client ko initialize karna
client = genai.Client(api_key=API_KEY)

def ask_gemini(question):
    """
    Sends the user query to Google Gemini LLM and returns a concise text response.
    """
    try:
        prompt = f"You are Jarvis, a witty and highly intelligent AI assistant. Answer this question concisely in 2-3 sentences max: {question}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"\n[GEMINI ERROR]: {e}\n")
        return "Sorry Boss, network network issue."