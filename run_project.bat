@echo off
title FT95 Thermometer System Loader
color 0A

:: 1. Project Folder ka rasta
set PROJECT_DIR=D:\all_info\all_data\other_folders\Development\ft95-thermometer-system

:: 2. Virtual Environment (venv) ka ASLI rasta jo aapke VS Code mein hai
set VENV_PYTHON=D:\all_info\all_data\other_folders\Development\venv\Scripts\python.exe

echo ====================================================
echo      FT95 SYSTEM IS STARTING (VS CODE PATH)
echo ====================================================
echo.

:: Project folder mein move karna
cd /d "%PROJECT_DIR%"

:: Purani python tasks ko khatam karna taake port 5000 free ho jaye
:: taskkill /F /IM python.exe /T >nul 2>&1

echo.
echo [STATUS] Connecting to Google Sheets...
echo [STATUS] Starting Flask Server on http://localhost:5000
echo.

:: VS Code wala exact python interpreter use karke run karna
"%VENV_PYTHON%" main.py

echo.
echo ----------------------------------------------------
echo System has stopped or crashed.
pause