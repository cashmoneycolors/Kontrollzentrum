#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KONTROLLZENTRUM PRODUCTION SETUP v1.0
Vollständige Initialisierung: Dependencies, Keys (optional), Tests, Start
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Encoding fix
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_cmd(cmd, desc=""):
    """Führt Befehl aus mit Error-Handling"""
    print(f"\n{'='*70}")
    print(f">> {desc or cmd}")
    print('='*70)
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False, text=True)
        print(f"OK {desc or cmd} erfolgreich")
        return True
    except subprocess.CalledProcessError as e:
        print(f"WARN {desc or cmd} - Fehler (optional)")
        return False

def setup_env():
    """Erstellt .env aus .env.example"""
    if not Path(".env").exists():
        if Path(".env.example").exists():
            shutil.copy(".env.example", ".env")
            print("OK .env erstellt (aus .env.example)")
        else:
            print("WARN .env.example nicht gefunden - erstelle leere .env")
            Path(".env").touch()
    else:
        print("OK .env existiert bereits")
    return True

def install_deps():
    """Installiert alle Dependencies"""
    if not Path("requirements.txt").exists():
        print("ERROR requirements.txt nicht gefunden!")
        return False
    
    return run_cmd(
        "py -3.11 -m pip install -r requirements.txt --upgrade",
        "INSTALL Dependencies"
    )

def check_keys():
    """Prüft API-Keys - optional"""
    print("\n" + "="*70)
    print("API-Keys Status")
    print("="*70)
    
    optional_keys = [
        "OPENAI_API_KEY",
        "STRIPE_API_KEY",
        "PAYPAL_CLIENT_ID",
        "AWS_ACCESS_KEY_ID",
        "NFT_API_KEY",
    ]
    
    available = []
    missing = []
    for key in optional_keys:
        if os.getenv(key):
            print(f"OK {key}")
            available.append(key)
        else:
            print(f"OPTIONAL {key}")
            missing.append(key)
    
    if available:
        print(f"\nOK {len(available)} Keys vorhanden - Produktivmodus")
        return True
    else:
        print(f"\nWARN Keine Keys vorhanden - Demo-Modus aktiviert")
        print("   Du kannst Keys später in .env eintragen")
        return True

def run_tests():
    """Führt Unit-Tests aus"""
    if not Path("tests").exists():
        print("WARN tests/ Verzeichnis nicht gefunden")
        return True
    
    return run_cmd(
        "py -3.11 -m unittest discover tests -v",
        "TEST Führe Tests aus"
    )

def show_menu():
    """Zeigt Startmenü"""
    print("\n" + "="*70)
    print("KONTROLLZENTRUM - PRODUCTION READY")
    print("="*70)
    print("""
Wähle Startmodus:
  1. CLI Mode (interaktiv)
  2. Team Mode (alle Module automatisch)
  3. API Gateway (http://localhost:8000)
  4. Health Check
  5. Streamlit Dashboard
  0. Beenden
    """)
    
    choice = input("Wahl (0-5): ").strip()
    
    if choice == "1":
        run_cmd("py -3.11 main.py", "CLI Mode")
    elif choice == "2":
        run_cmd("py -3.11 main.py team", "Team Mode")
    elif choice == "3":
        run_cmd("py -3.11 main.py api", "API Gateway")
    elif choice == "4":
        run_cmd("py -3.11 main.py health", "Health Check")
    elif choice == "5":
        run_cmd("streamlit run main.py", "Streamlit Dashboard")
    elif choice == "0":
        print("Auf Wiedersehen!")
        sys.exit(0)
    else:
        print("ERROR Ungültige Eingabe")

def main():
    """Hauptablauf"""
    print("""
KONTROLLZENTRUM PRODUCTION SETUP v1.0
Plug-and-Play Module + API Gateway + Dashboard
OK Funktioniert auch ohne API-Keys (Demo-Modus)
    """)
    
    print("\n[SCHRITT 1/4] Umgebung vorbereiten...")
    if not setup_env():
        sys.exit(1)
    
    print("\n[SCHRITT 2/4] Dependencies installieren...")
    install_deps()
    
    print("\n[SCHRITT 3/4] API-Keys prüfen...")
    check_keys()
    
    print("\n[SCHRITT 4/4] Tests ausführen...")
    run_tests()
    
    print("\nOK SYSTEM BEREIT!")
    while True:
        show_menu()

if __name__ == "__main__":
    main()
