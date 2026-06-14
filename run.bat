@echo off
REM Quick Start Script for SEO Content Generator

echo.
echo ========================================
echo SEO Content Generator - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Installing dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Checking Google credentials...
if not exist "secrets\google-service-account.json" (
    echo WARNING: Google credentials not found at secrets\google-service-account.json
    echo Please add your Google service account JSON file
)

echo.
echo [4/4] Starting application...
echo.
echo ========================================
echo Server is starting...
echo Admin Panel: http://localhost:8000/admin
echo API Docs:   http://localhost:8000/docs
echo ========================================
echo.

python app/main.py
