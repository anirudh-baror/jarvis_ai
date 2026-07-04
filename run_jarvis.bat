@echo off
title Launching Jarvis AI...
echo [INFO] Activating Virtual Environment (.venv)...
call .venv\Scripts\activate

echo [INFO] Launching Main System Pipeline...
python main.py

echo.
echo [INFO] Jarvis has stopped executing.
pause