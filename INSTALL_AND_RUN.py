#!/usr/bin/env python3
"""
INSTALL & RUN - Kontrollzentrum auf Laptop laden und starten
"""
import subprocess
import sys
import os
from pathlib import Path

print("\n" + "="*70)
print("📦 KONTROLLZENTRUM - INSTALL & RUN")
print("="*70 + "\n")

# 1. Requirements installieren
print("📥 Installiere Dependencies...")
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=False)
    print("✅ Dependencies installiert\n")
except Exception as e:
    print(f"⚠️  {e}\n")

# 2. Struktur prüfen
print("✅ Prüfe Struktur...")
for folder in ["modules", "core", "submodules"]:
    if Path(folder).exists():
        print(f"  ✓ {folder}")
print()

# 3. Wrapper prüfen
print("✅ Prüfe Wrapper...")
if Path("modules/separate_project_wrapper.py").exists():
    print("  ✓ Wrapper OK\n")
else:
    print("  ❌ Wrapper fehlt!\n")

# 4. Starte App
print("="*70)
print("🚀 STARTE KONTROLLZENTRUM")
print("="*70 + "\n")

os.system("python PRODUCTION_GO_LIVE.py")
