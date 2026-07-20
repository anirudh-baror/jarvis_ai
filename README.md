# Jarvis AI — Bilingual Voice Assistant with Autonomous Tool Use

Jarvis is a modular, AI-native personal assistant built on Google's Gemini LLM. It understands and responds fluently in English, Hindi, and Hinglish, remembers conversation context across sessions, and autonomously decides when to trigger real-world actions — such as opening YouTube or searching Google — using Gemini's native function calling rather than brittle keyword matching. The project is available both as a voice-controlled desktop assistant and as a browser-based chat interface built with Streamlit.

---

## Table of Contents

- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Extending Jarvis: The Plugin System](#extending-jarvis-the-plugin-system)
- [Security Practices](#security-practices)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Key Features

### 🌐 Bilingual, Context-Aware Conversation
Jarvis detects the language of the user's query and responds in kind — in English, Hindi (written in Roman script for compatibility with speech engines), or natural Hinglish — powered by carefully engineered system prompts rather than a separate translation layer.

### 🎙️ Natural Voice Interaction
Speech input is captured via `SpeechRecognition`, with an automatic fallback chain that attempts English recognition first and falls back to Hindi if the first pass fails — allowing a single voice pipeline to handle both languages. Responses are spoken aloud using Google Text-to-Speech (gTTS), replacing the earlier robotic, English-only Windows-native voice engine.

### 🧠 Persistent Conversation Memory
Conversations are stored in a local SQLite database (`ai/memory.py`). Each time Jarvis is queried, it retrieves the most recent exchanges and includes them as context in its prompt to Gemini — allowing it to recall facts the user has shared earlier in the session (e.g. their name or preferences) instead of treating every query in isolation.

### 🛠️ Autonomous Function Calling
Rather than routing commands through hardcoded `if/elif` string matching, Jarvis uses Gemini's native function-calling capability. Python functions are exposed to the model as callable tools, along with descriptive docstrings; Gemini itself decides — based on natural language understanding — whether a user's request should trigger a tool (like opening YouTube) or be answered directly as a general-knowledge question. This makes the assistant significantly more robust to varied, real-world phrasing.

### 🔌 Auto-Discovering Plugin System
New capabilities can be added to Jarvis without touching any core logic. Any Python file placed inside the `plugins/` directory is automatically discovered, imported, and exposed to Gemini as an available tool via a dynamic loader (`plugins/loader.py`), built using Python's `pkgutil`, `importlib`, and `inspect` modules.

### 💬 Web-Based Chat Interface
In addition to the voice assistant, Jarvis ships with a Streamlit-based chat interface (`app.py`) offering a familiar, ChatGPT-style browsing experience — complete with message history within a session — for users who prefer typing over speaking.

### 🌍 Web Automation
Jarvis can open YouTube, search and play content on YouTube, and perform Google searches on the user's behalf, with all query strings safely URL-encoded to prevent malformed requests.

---

## Architecture Overview

Jarvis follows a decoupled, modular architecture, with responsibilities cleanly separated into independent Python packages rather than a single monolithic script:

```
User Input (Voice or Text)
        │
        ▼
 Intent Handling (main.py / app.py)
        │
        ▼
  Gemini Client (ai/gemini_client.py)
   ├── Injects conversation history (ai/memory.py)
   ├── Exposes available tools (automation/ + plugins/)
   └── Applies bilingual system instructions
        │
        ▼
  Gemini decides: answer directly, OR call a tool
        │
   ┌────┴─────┐
   ▼          ▼
Text Reply   Tool Execution (browser automation, plugins)
        │
        ▼
Spoken (voice/speaker.py) or Displayed (Streamlit)
```

This separation means a bug in the audio-capture layer cannot affect the LLM client, and new capabilities can be added to the `plugins/` package without modifying the core assistant logic at all.

---

## Project Structure

```
jarvis_ai/
│
├── ai/
│   ├── __init__.py
│   ├── gemini_client.py      # Gemini API client, system prompt, tool orchestration
│   └── memory.py             # SQLite-backed conversation history
│
├── automation/
│   ├── __init__.py
│   └── browser.py            # YouTube / Google Search automation tools
│
├── voice/
│   ├── __init__.py
│   ├── listener.py           # Speech-to-text (English + Hindi fallback)
│   └── speaker.py            # Text-to-speech via gTTS
│
├── plugins/
│   ├── __init__.py
│   ├── loader.py             # Auto-discovers and loads plugin tools
│   └── get_time.py           # Sample plugin: returns the current time
│
├── .env                      # API keys (excluded from version control)
├── .gitignore
├── app.py                    # Streamlit web chat interface
├── config.py                 # Global constants and fallback configuration
├── main.py                   # Entry point for the voice assistant
├── requirements.txt
└── run_jarvis.bat            # Windows launcher script
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Language Model | Google Gemini (`gemini-2.5-flash`) via `google-genai` SDK |
| Language | Python 3.12 |
| Speech Recognition | `SpeechRecognition` (Google Speech API) |
| Text-to-Speech | `gTTS` (Google Text-to-Speech) |
| Database | SQLite (built-in, no external server) |
| Web Interface | Streamlit |
| Environment Management | `python-dotenv` |
| Version Control | Git / GitHub |

---

## How It Works

1. **Input capture** — The user speaks (voice mode) or types (web mode) a query.
2. **Context retrieval** — The most recent exchanges are pulled from the SQLite memory store to give Gemini conversational context.
3. **Tool-aware reasoning** — The query, conversation history, and a list of available tools (browser automation functions plus any auto-discovered plugins) are sent to Gemini along with a system instruction defining Jarvis's persona, language behavior, and rules for when tool use is and isn't appropriate.
4. **Decision** — Gemini either responds directly (for general knowledge or conversation) or invokes the relevant Python function automatically.
5. **Output** — The response is spoken aloud (voice mode) or rendered in the chat window (web mode), and the exchange is persisted to memory for future context.

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/apikey))
- Windows OS (for the native voice launcher script; the Streamlit interface is cross-platform)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/anirudh-baror/jarvis_ai.git
   cd jarvis_ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

---

## Usage

### Voice Assistant Mode
```bash
python main.py
```
Or on Windows, simply double-click `run_jarvis.bat`. Speak your query after the "Listening..." prompt appears. Say "stop", "exit", or "bye" to end the session.

### Web Chat Interface
```bash
streamlit run app.py
```
This launches a browser-based chat interface at `http://localhost:8501`, where you can type messages to Jarvis and receive responses in a familiar chat format.

---

## Extending Jarvis: The Plugin System

Adding a new capability to Jarvis requires no changes to the core application. Simply create a new Python file inside the `plugins/` directory containing one or more functions with clear docstrings describing their purpose:

```python
# plugins/my_new_tool.py

def my_new_function(parameter: str):
    """A clear description of what this tool does and when to use it.

    Args:
        parameter: Description of the expected input.
    """
    # implementation
    return "result"
```

On the next run, `plugins/loader.py` automatically discovers, imports, and registers the new function as an available tool for Gemini — no manual wiring required.

---

## Security Practices

- API keys are stored exclusively in a local `.env` file, loaded via `python-dotenv`, and never committed to version control (`.env` is listed in `.gitignore`).
- The local conversation memory database (`memory.db`) is also excluded from version control, as it may contain personal conversational data.
- `config.py` contains only a non-functional placeholder fallback and is not used to store real credentials.

---

## Roadmap

- [ ] Multi-conversation support with a session sidebar in the Streamlit interface (ChatGPT-style conversation switching)
- [ ] Additional plugins (system control, weather, reminders)
- [ ] Streaming responses in the web interface
- [ ] Cross-platform launcher scripts (macOS/Linux)

---

## Author

**Anirudh Baror**
GitHub: [@anirudh-baror](https://github.com/anirudh-baror)

---

*This project was built as a hands-on exploration of LLM-native application design — including prompt engineering, autonomous tool use, and extensible plugin architectures — using Google's Gemini API.*
