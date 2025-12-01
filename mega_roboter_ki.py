#!/usr/bin/env python3
"""MegaRoboterKI - Autonomer Setup & Test Wizard"""
import os
import subprocess
import shutil
from pathlib import Path

def ensure_structure():
    """Projektstruktur prüfen und anlegen"""
    for folder in ["modules", "core", "tests", ".github"]:
        Path(folder).mkdir(exist_ok=True)
    if not Path(".env").exists() and Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
    print("[✅] Projektstruktur geprüft und angelegt.")

def install_requirements():
    """Abhängigkeiten installieren"""
    if Path("requirements.txt").exists():
        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            print("[✅] Abhängigkeiten installiert.")
        except subprocess.CalledProcessError as e:
            print(f"[❌] Fehler beim Installieren: {e}")
    else:
        print("[⚠️] requirements.txt fehlt.")

def test_modules():
    """Unittests ausführen"""
    print("[ℹ️] Starte Unittests...")
    try:
        subprocess.run(["python", "-m", "unittest", "discover", "tests"], check=False)
    except Exception as e:
        print(f"[⚠️] Fehler beim Testen: {e}")

def test_api():
    """API-Integration testen"""
    print("[ℹ️] API-Integration wird überprüft...")
    print("[ℹ️] Starte main.py im CLI-Modus...")
    try:
        subprocess.run(["python", "main.py"], timeout=5, check=False)
    except subprocess.TimeoutExpired:
        print("[ℹ️] CLI-Modus läuft (Timeout erwartet)")
    except Exception as e:
        print(f"[⚠️] Fehler: {e}")

def backup():
    """Backup erstellen"""
    try:
        backup_name = f"backup_kontrollzentrum"
        shutil.make_archive(backup_name, 'zip', '.')
        print(f"[✅] Backup erstellt: {backup_name}.zip")
    except Exception as e:
        print(f"[❌] Backup-Fehler: {e}")

def check_keys():
    """API-Keys prüfen"""
    print("[ℹ️] Prüfe API-Keys...")
    try:
        from core.key_check import check_all_keys
        check_all_keys()
        print("[✅] Alle API-Keys vorhanden!")
    except RuntimeError as e:
        print(f"[⚠️] {e}")

def main():
    """Hauptmenü"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  🤖 MegaRoboterKI – Kontrollzentrum Autonomer Modus       ║
╚════════════════════════════════════════════════════════════╝

1. 📁 Struktur prüfen
2. 📦 Abhängigkeiten installieren
3. 🧪 Module testen
4. 🌐 API-Integration testen
5. 💾 Backup erstellen
6. 🔑 API-Keys prüfen
0. ❌ Beenden
    """)
    
    while True:
        try:
            wahl = input("Aktion wählen (0-6): ").strip()
            if wahl == "1":
                ensure_structure()
            elif wahl == "2":
                install_requirements()
            elif wahl == "3":
                test_modules()
            elif wahl == "4":
                test_api()
            elif wahl == "5":
                backup()
            elif wahl == "6":
                check_keys()
            elif wahl == "0":
                print("[✅] Auf Wiedersehen!")
                break
            else:
                print("[❌] Ungültige Eingabe!")
        except KeyboardInterrupt:
            print("\n[⚠️] Abgebrochen.")
            break
        except Exception as e:
            print(f"[❌] Fehler: {e}")

if __name__ == "__main__":
    main()
