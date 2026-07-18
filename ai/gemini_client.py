from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import config
from ai.memory import save_message, get_recent_history
from automation.browser import open_youtube, play_on_youtube, search_google

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY

client = genai.Client(api_key=API_KEY)

# Jarvis's personality and behavior rules
SYSTEM_INSTRUCTION = (
    "You are Jarvis, a witty and highly intelligent AI assistant with broad "
    "general knowledge on any topic that exists in the world. "
    "Always reply in the SAME language the user used. "
    "If the user asks in Hindi, reply in Hindi but written in Roman/English letters "
    "(do not use Devanagari script), e.g. 'Bharat ki rajdhani Nai Dilli hai'. "
    "If the user asks in English, reply in English. "
    "If the user asks in Hinglish, reply in the same Hinglish style. "
    "Never refuse a general-knowledge question — answer confidently. "
    "You have access to tools for opening YouTube, playing something on YouTube, "
    "and searching Google. Use the right tool whenever the user's request matches it. "
    "After using a tool, briefly confirm what you did in one short sentence."
)

def ask_gemini(question):
    """
    Sends the user query to Gemini along with recent conversation history.
    Gemini can automatically call browser automation tools (YouTube, Google search)
    when the user's request matches, or answer directly as a normal question.
    """
    try:
        history = get_recent_history(limit=6)
        history_text = ""
        for role, message in history:
            speaker = "User" if role == "user" else "Jarvis"
            history_text += f"{speaker}: {message}\n"

        prompt = (
            f"Conversation history:\n{history_text}\n"
            f"New message: {question}\n"
            "Respond concisely in 2-3 sentences max."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[open_youtube, play_on_youtube, search_google],
            ),
        )
        answer = response.text

        save_message("user", question)
        save_message("assistant", answer)

        return answer
    except Exception as e:
        print(f"\n[GEMINI ERROR]: {e}\n")
        return "Sorry Boss, network network issue."