from google import genai
from dotenv import load_dotenv
import os
import config
from ai.memory import save_message, get_recent_history

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY

client = genai.Client(api_key=API_KEY)

def ask_gemini(question):
    """
    Sends the user query to Google Gemini LLM, along with recent
    conversation history for context, and returns a concise,
    bilingual (Hindi + English) text response.
    """
    try:
        # Fetch recent conversation history for context
        history = get_recent_history(limit=6)
        history_text = ""
        for role, message in history:
            speaker = "User" if role == "user" else "Jarvis"
            history_text += f"{speaker}: {message}\n"

        prompt = (
            "You are Jarvis, a witty and highly intelligent AI assistant with broad "
            "general knowledge on any topic that exists in the world. "
            "Always reply in the SAME language the user used. "
            "If the user asks in Hindi, reply in Hindi but written in Roman/English letters "
            "(do not use Devanagari script), e.g. 'Bharat ki rajdhani Nai Dilli hai'. "
            "If the user asks in English, reply in English. "
            "If the user asks in Hinglish, reply in the same Hinglish style. "
            "Never refuse a general-knowledge question — answer confidently. "
            "Use the conversation history below to remember context (like the user's name, "
            "preferences, or earlier topics) if relevant.\n\n"
            f"Conversation history:\n{history_text}\n"
            f"New question: {question}\n"
            "Answer this concisely in 2-3 sentences max."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        answer = response.text

        # Save the new exchange to memory
        save_message("user", question)
        save_message("assistant", answer)

        return answer
    except Exception as e:
        print(f"\n[GEMINI ERROR]: {e}\n")
        return "Sorry Boss, network network issue."