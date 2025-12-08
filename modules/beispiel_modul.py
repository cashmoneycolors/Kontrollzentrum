"""
Beispiel-Modul - Template für neue Module
Funktioniert auch ohne API-Keys (Demo-Modus)
"""
from core.key_check import has_key
import datetime

def run():
    """Hauptfunktion - wird vom Kontrollzentrum aufgerufen"""
    mode = "Produktiv" if has_key("OPENAI_API_KEY") else "Demo"
    
    return {
        "status": "ok",
        "message": f"Beispiel-Modul erfolgreich ausgeführt ({mode}-Modus)",
        "timestamp": datetime.datetime.now().isoformat(),
        "mode": mode
    }

def install():
    """Optional: Installation/Setup"""
    print("✅ Beispiel-Modul installiert")

def describe():
    """Beschreibung des Moduls"""
    return "Generisches Test-Modul mit run()-Funktion (Demo + Produktiv)"
