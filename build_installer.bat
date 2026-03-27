@echo off
echo ========================================
echo Asset Manager - Installer Build Script
echo ========================================
echo.

REM Check if executable exists
if not exist "dist\AssetManager.exe" (
    echo Error: Executable not found at dist\AssetManager.exe
    echo Please run build_all.bat first to create the executable.
    pause
    exit /b 1
)

REM Check if Inno Setup is installed
iscc /? >nul 2>&1
if errorlevel 1 (
    echo Error: Inno Setup not found.
    echo Please install Inno Setup from:
    echo https://jrsoftware.org/isinfo.php
    echo Then add it to your PATH.
    pause
    exit /b 1
)

echo Building installer...
iscc setup.iss
if errorlevel 1 (
    echo Error: Failed to build installer
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installer created: installer\AssetManagerSetup.exe
echo ========================================
echo.
pause