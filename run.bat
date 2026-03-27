@echo off
echo Starting Asset Manager...
C:/Users/dell/AppData/Local/Programs/Python/Python314/python.exe main.py
if errorlevel 1 (
    echo.
    echo Error: Failed to start Asset Manager.
    echo Make sure Python and required packages are installed.
    echo Run: pip install -r requirements.txt
    pause
)
