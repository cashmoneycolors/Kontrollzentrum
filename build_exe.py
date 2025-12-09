#!/usr/bin/env python3
"""Build ROBOTER_KI_APP.exe with PyInstaller"""
import subprocess
import sys
import os

print("🚀 Building ROBOTER_KI_APP.exe...")

# Install PyInstaller
subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"])

# Build EXE
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--icon=icon.ico",
    "--name=ROBOTER_KI_APP",
    "--distpath=dist",
    "--buildpath=build",
    "--specpath=.",
    "main.py"
])

print("✅ EXE erstellt: dist/ROBOTER_KI_APP.exe")
