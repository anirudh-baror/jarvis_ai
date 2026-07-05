# Jarvis AI - Advanced Voice Assistant & Search Engine

An intelligent, modular voice assistant powered by the Google Gemini AI flagship model, integrated with custom automation engines for seamless hands-free desktop and web operations.

---

## 📅 Project Timeline & Milestone Log

* **Project Commencement:** June 28, 2026
* **Core Architecture Unified:** July 5, 2026
* **Status:** Phase 1 (Core AI + Web Automation) Fully Operational & Stable.

---

## 🚀 Features Built & Implemented

### 1. Unified Intent Routing Engine (`main.py`)
* Implemented a structural control loop that dynamically intercepts user voice inputs.
* Built token-saving routing filters that separate pure system/automation requests from complex open-ended cognitive queries.

### 2. Conversational Generative AI (`ai/`)
* Integrated the official, production-grade `google-genai` SDK configuration.
* Established a localized client structure (`gemini_client.py`) utilizing standard industrial exception handling to guarantee consistent uptime.

### 3. Integrated Web Search & Automation Engine (`automation/`)
* Implemented headless/automated browsing redirection layers for Google Search indexes and YouTube automation.
* Utilized `urllib.parse.quote_plus` to automatically sanitize and encode verbal inputs into standard web-safe URL formats, completely eliminating injection errors.

### 4. Advanced Production Architecture
* Complete project decoupling into strictly defined sub-packages (`ai/`, `voice/`, `automation/`).
* Implemented strict environment variable masks (`.env` parsing via `.gitignore`) ensuring critical project credentials and Gemini API keys are never leaked to public repositories.

---

## 📂 Project Structure Blueprint

```text
jarvis_ai/
│
├── ai/
│   ├── __init__.py
│   └── gemini_client.py
├── automation/
│   ├── __init__.py
│   └── browser.py
├── voice/
│   ├── __init__.py
│   ├── listener.py
│   └── speaker.py
├── .env                  [Secured / Locally Masked]
├── .gitignore            [Git Track Exclusion Rules]
├── config.py             [Global Constants & Configs]
├── main.py               [Main Execution Hub]
├── README.md             [Project Documentation]
├── requirements.txt      [Environment Dependencies]
└── run_jarvis.bat        [Windows Terminal Shortcut Launcher]