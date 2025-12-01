# 👨‍💻 Developer Guide - Neue Module erstellen

## 🚀 Schnellstart (5 Minuten)

### 1. Modul-Template kopieren
```bash
cp modules/TEMPLATE_modul.py modules/mein_modul.py
```

### 2. Modul implementieren
```python
from core.key_check import require_keys

@require_keys
def run(*args):
    return {"status": "success", "data": "Meine Daten"}

def describe():
    return "Mein Modul - Beschreibung"
```

### 3. Testen
```bash
python main.py alle run
# Dein Modul wird automatisch erkannt!
```

---

## 📋 Modul-Struktur

### Erforderlich
```python
@require_keys
def run(*args):
    """Haupteinstiegspunkt"""
    return result
```

### Optional
```python
def install():
    """Installations-Routine"""
    pass

def describe():
    """Modul-Beschreibung"""
    return "Beschreibung"

def to_svg():
    """SVG-Export"""
    pass

def to_word():
    """Word-Export"""
    pass
```

---

## 🔑 API-Keys verwenden

### Einfach
```python
from core.key_check import require_keys
import os

@require_keys
def run():
    api_key = os.getenv("OPENAI_API_KEY")
    # Deine Logik
```

### Mit Fehlerbehandlung
```python
@require_keys
def run():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY fehlt!")
    # Deine Logik
```

---

## 🌐 FastAPI-Modul erstellen

```python
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Mein API")

class MyRequest(BaseModel):
    data: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/process")
async def process(request: MyRequest):
    return {"result": request.data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

**Starten:**
```bash
python modules/mein_modul.py
# http://localhost:8004/docs
```

---

## 🧪 Tests schreiben

### Unit-Test
```python
# tests/test_mein_modul.py
import unittest
from modules.mein_modul import run

class TestMeinModul(unittest.TestCase):
    def test_run(self):
        result = run()
        self.assertEqual(result["status"], "success")

if __name__ == "__main__":
    unittest.main()
```

**Ausführen:**
```bash
python -m unittest tests.test_mein_modul -v
```

---

## 📦 Dependencies hinzufügen

### 1. requirements.txt aktualisieren
```
requests>=2.31.0
pandas>=2.0.0
```

### 2. Installieren
```bash
pip install -r requirements.txt
```

### 3. Im Modul verwenden
```python
import requests
import pandas as pd
```

---

## 🎯 Best Practices

### ✅ DO
- Verwende `@require_keys` auf produktiven Funktionen
- Schreibe aussagekräftige Fehlermeldungen
- Dokumentiere dein Modul mit `describe()`
- Schreibe Unit-Tests
- Nutze `.env` für Secrets

### ❌ DON'T
- Hardcode API-Keys
- Verwende Demo-Modi
- Ignoriere fehlende Keys
- Schreibe Secrets in Logs
- Committen `.env`

---

## 🔄 Modul-Lifecycle

```
1. Erstellen: modules/mein_modul.py
   ↓
2. Implementieren: run(), install(), describe()
   ↓
3. Testen: python -m unittest tests.test_mein_modul
   ↓
4. Auto-Discovery: python main.py alle run
   ↓
5. Dashboard: streamlit run main.py
```

---

## 📊 Modul-Beispiele

### Einfaches Modul
```python
from core.key_check import require_keys

@require_keys
def run(*args):
    return {"status": "success"}
```

### Mit Daten-Verarbeitung
```python
import pandas as pd

@require_keys
def run(data=None):
    if data:
        df = pd.DataFrame(data)
        return {"rows": len(df)}
    return {"rows": 0}
```

### Mit API-Call
```python
import requests

@require_keys
def run():
    response = requests.get("https://api.example.com/data")
    return response.json()
```

### Mit FastAPI
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
async def get_data():
    return {"data": "value"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

---

## 🐛 Debugging

### Modul einzeln testen
```bash
python -c "from modules.mein_modul import run; print(run())"
```

### Mit Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

@require_keys
def run():
    logging.debug("Modul startet...")
    # Deine Logik
```

### Mit Breakpoint
```python
@require_keys
def run():
    breakpoint()  # Debugger stoppt hier
    # Deine Logik
```

---

## 📚 Weitere Ressourcen

- `QUICKSTART.md` - Projekt-Übersicht
- `FINAL_STATUS.md` - Projekt-Status
- `modules/TEMPLATE_modul.py` - Modul-Template
- `.github/copilot-instructions.md` - AI-Agent-Anleitung

---

**Happy Coding! 🚀**

*Letzte Aktualisierung: 2025-11-30*
