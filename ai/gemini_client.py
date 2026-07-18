from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import config
from ai.memory import save_message, get_recent_history
from automation.browser import open_youtube, play_on_youtube, search_google
from plugins.loader import load_all_plugins

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY

client = genai.Client(api_key=API_KEY)

ALL_TOOLS = [open_youtube, play_on_youtube, search_google] + load_all_plugins()

SYSTEM_INSTRUCTION = (
    "You are Jarvis, a witty and highly intelligent AI assistant with broad "
    "general knowledge on any topic that exists in the world. "
    "Always reply in the SAME language the user used. "
    "If the user asks in Hindi, reply in Hindi but written in Roman/English letters "
    "(do not use Devanagari script), e.g. 'Bharat ki rajdhani Nai Dilli hai'. "
    "If the user asks in English, reply in English. "
    "If the user asks in Hinglish, reply in the same Hinglish style. "
    "You have access to tools for opening YouTube, playing something on YouTube, "
    "searching Google, and getting the current time. "
    "IMPORTANT: Only use a tool when the user's request clearly and explicitly "
    "matches what that tool does (e.g. they say 'open youtube', 'play a song', "
    "'search on google', or 'what time is it'). "
    "For ALL general knowledge questions (facts, capitals, history, science, "
    "definitions, opinions, etc.) — even if you could technically search for them — "
    "answer directly from your own knowledge. Do NOT use the Google search tool "
    "for questions you already know the answer to. Never refuse a general-knowledge "
    "question — answer confidently from your own knowledge. "
    "After using a tool, briefly confirm what you did in one short sentence."
)

def ask_gemini(question):
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
                tools=ALL_TOOLS,
            ),
        )
        answer = response.text

        save_message("user", question)
        save_message("assistant", answer)

        return answer
    except Exception as e:
        print(f"\n[GEMINI ERROR]: {e}\n")
        return "Sorry Boss, network network issue."