#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Startet alle 5 Modi der Reihe nach
"""
import subprocess
import sys
import time

modes = [
    ("1", "CLI Mode", "py -3.11 main.py"),
    ("2", "Team Mode", "py -3.11 main.py team"),
    ("3", "API Gateway", "py -3.11 main.py api"),
    ("4", "Health Check", "py -3.11 main.py health"),
    ("5", "Streamlit Dashboard", "streamlit run main.py"),
]

print("="*70)
print("STARTE ALLE 5 MODI DER REIHE NACH")
print("="*70)

for num, name, cmd in modes:
    print(f"\n[{num}/5] Starte {name}...")
    print(f"Befehl: {cmd}")
    print("-"*70)
    
    try:
        subprocess.run(cmd, shell=True, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT nach 30 Sekunden")
    except KeyboardInterrupt:
        print(f"Abgebrochen")
        break
    except Exception as e:
        print(f"Fehler: {e}")
    
    print(f"[{num}/5] {name} abgeschlossen")
    time.sleep(2)

print("\n" + "="*70)
print("ALLE MODI ABGESCHLOSSEN")
print("="*70)
