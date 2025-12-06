#!/usr/bin/env python3
"""
🚀 KONTROLLZENTRUM - PRODUCTION LAUNCH
========================================
Vollautomatischer Start aller Systeme
"""

import sys
import os
import subprocess
import time
import threading
from datetime import datetime

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def check_env():
    """Prüft .env Datei"""
    if not os.path.exists(".env"):
        log("⚠️  .env nicht gefunden - erstelle mit Defaults", "WARN")
        with open(".env", "w") as f:
            f.write("ENVIRONMENT=production\n")
            f.write("DEBUG=false\n")
    log("✅ .env konfiguriert")

def check_dependencies():
    """Prüft kritische Dependencies"""
    deps = ["streamlit", "uvicorn", "sqlalchemy", "pandas"]
    missing = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        log(f"⚠️  Fehlende Dependencies: {', '.join(missing)}", "WARN")
        log("Installiere mit: pip install -r requirements.txt", "INFO")
    else:
        log("✅ Alle Dependencies vorhanden")

def start_team_mode():
    """Startet Team-Modus (alle Module)"""
    log("🔄 Starte Team-Modus...", "START")
    subprocess.run([sys.executable, "main.py", "team"])

def start_api_gateway():
    """Startet API Gateway in separatem Thread"""
    log("🔄 Starte API Gateway...", "START")
    def run_api():
        subprocess.run([sys.executable, "main.py", "api"])
    thread = threading.Thread(target=run_api, daemon=True)
    thread.start()
    time.sleep(2)
    log("✅ API Gateway läuft auf http://0.0.0.0:8000")

def start_health_monitor():
    """Startet Health Monitor"""
    log("🔄 Starte Health Monitor...", "START")
    subprocess.run([sys.executable, "main.py", "health"])

def production_menu():
    """Interaktives Produktions-Menü"""
    while True:
        print("\n" + "="*50)
        print("🎛️  KONTROLLZENTRUM - PRODUCTION MENU")
        print("="*50)
        print("1. 🚀 Team-Modus (alle Module)")
        print("2. 🌐 API Gateway starten")
        print("3. 🏥 Health Check")
        print("4. 📊 Dashboard (Streamlit)")
        print("5. 🔧 CLI Mode")
        print("6. ❌ Beenden")
        print("="*50)
        
        choice = input("Wähle Option (1-6): ").strip()
        
        if choice == "1":
            start_team_mode()
        elif choice == "2":
            start_api_gateway()
        elif choice == "3":
            start_health_monitor()
        elif choice == "4":
            log("🔄 Starte Streamlit Dashboard...", "START")
            subprocess.run(["streamlit", "run", "main.py"])
        elif choice == "5":
            log("🔄 Starte CLI Mode...", "START")
            subprocess.run([sys.executable, "main.py"])
        elif choice == "6":
            log("👋 Auf Wiedersehen!", "INFO")
            break
        else:
            log("❌ Ungültige Option", "ERROR")

def main():
    log("="*50, "INFO")
    log("🚀 KONTROLLZENTRUM v5.0 - PRODUCTION START", "INFO")
    log("="*50, "INFO")
    
    check_env()
    check_dependencies()
    
    log("✅ System bereit für produktiven Betrieb", "SUCCESS")
    log("", "INFO")
    
    production_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⏹️  Betrieb beendet", "INFO")
        sys.exit(0)
    except Exception as e:
        log(f"❌ Fehler: {e}", "ERROR")
        sys.exit(1)
