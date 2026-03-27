"""
Build script for Asset Manager application.
Creates a standalone executable using PyInstaller.
"""

import PyInstaller.__main__
import os
import sys

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# PyInstaller arguments
args = [
    'main.py',  # Main script
    '--name=AssetManager',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--windowed',  # No console window (GUI app)
    '--icon=icon.ico' if os.path.exists('icon.ico') else '',  # Icon if available
    '--add-data=assets.db;.',  # Include database file
    '--clean',  # Clean cache
    '--noconfirm',  # Don't ask for confirmation
]

# Remove empty arguments
args = [arg for arg in args if arg]

print("Building Asset Manager executable...")
print(f"Arguments: {args}")

# Run PyInstaller
PyInstaller.__main__.run(args)

print("\nBuild complete!")
print("Executable location: dist/AssetManager.exe")
