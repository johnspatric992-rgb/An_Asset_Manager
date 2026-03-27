@echo off
echo ========================================
echo Asset Manager - Build Script
echo ========================================
echo.

REM Check if Python is installed
C:/Users/dell/AppData/Local/Programs/Python/Python314/python.exe --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
C:/Users/dell/AppData/Local/Programs/Python/Python314/python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Installing PyInstaller...
C:/Users/dell/AppData/Local/Programs/Python/Python314/python.exe -m pip install pyinstaller
if errorlevel 1 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/5] Building executable...
C:/Users/dell/AppData/Local/Programs/Python/Python314/python.exe -m pyinstaller --onefile --windowed --name=AssetManager --clean --noconfirm main.py
if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo [4/5] Checking for Inno Setup...
iscc /? >nul 2>&1
if errorlevel 1 (
    echo Warning: Inno Setup not found. Installer will not be built.
    echo To build the installer, install Inno Setup from:
    echo https://jrsoftware.org/isinfo.php
    echo Then add it to your PATH or run this script from Inno Setup's directory.
    goto :skip_installer
)

echo.
echo [5/5] Building installer...
iscc setup.iss
if errorlevel 1 (
    echo Error: Failed to build installer
    pause
    exit /b 1
)

:skip_installer
echo.
echo Build complete!
echo.
echo ========================================
echo Executable created: dist\AssetManager.exe
if exist "installer\AssetManagerSetup.exe" (
    echo Installer created: installer\AssetManagerSetup.exe
)
echo ========================================
echo.
echo You can now:
echo 1. Run dist\AssetManager.exe directly
if exist "installer\AssetManagerSetup.exe" (
    echo 2. Run installer\AssetManagerSetup.exe to install the application
)
echo 2. Create an installer using Inno Setup (setup.iss)
echo.
pause
