#!/usr/bin/env python3
import sys
import os

os.chdir(r'c:\Users\Laptop\Kontrollzentrum-1')
sys.path.insert(0, r'c:\Users\Laptop\Kontrollzentrum-1')

print("\n🚀 KONTROLLZENTRUM STARTET...\n")

from main import run_team_mode
run_team_mode()

print("\n✅ FERTIG!\n")
