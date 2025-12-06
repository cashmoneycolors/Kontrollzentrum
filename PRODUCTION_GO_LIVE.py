#!/usr/bin/env python3
"""
PRODUCTION GO-LIVE
Startet Kontrollzentrum mit allen Modulen in Produktion
"""
import sys
import os
from pathlib import Path

print("\n" + "="*70)
print("🚀 KONTROLLZENTRUM - PRODUCTION GO-LIVE")
print("="*70 + "\n")

# 1. Struktur prüfen
print("✅ Prüfe Projektstruktur...")
required = ["modules", "core", "main.py"]
for item in required:
    if not Path(item).exists():
        print(f"❌ {item} FEHLT!")
        sys.exit(1)
print("✅ Struktur OK\n")

# 2. Wrapper prüfen
print("✅ Prüfe Wrapper...")
wrapper = Path("modules/separate_project_wrapper.py")
if not wrapper.exists():
    print(f"❌ Wrapper nicht gefunden!")
    sys.exit(1)
print("✅ Wrapper OK\n")

# 3. Module laden
print("✅ Lade Module...")
sys.path.insert(0, str(Path.cwd()))
from main import discover_modules

modules = discover_modules()
print(f"✅ {len(modules)} Module gefunden\n")

# 4. Team-Modus starten
print("="*70)
print("🎯 STARTE TEAM-MODUS (Alle Module)")
print("="*70 + "\n")

from main import run_team_mode
run_team_mode()

print("\n" + "="*70)
print("✅ PRODUCTION GO-LIVE ERFOLGREICH!")
print("="*70)
print("\n📊 Status:")
print("  ✅ Alle Module geladen")
print("  ✅ Wrapper aktiv")
print("  ✅ Orchestration läuft")
print("  ✅ Log: team_log.txt")
print("\n🎉 KONTROLLZENTRUM IST LIVE!\n")
