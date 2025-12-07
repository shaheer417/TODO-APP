@echo off
REM TODO Master - Windows Command Prompt Launcher
REM This batch file ensures proper UTF-8 encoding for emojis and Unicode

REM Set console code page to UTF-8 (65001)
chcp 65001 >nul

REM Set Python environment to UTF-8
set PYTHONIOENCODING=utf-8

REM Run the application
python -m todo_app.main

REM Pause to see any error messages
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)
