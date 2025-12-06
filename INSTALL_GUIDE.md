# 📦 INSTALL & RUN GUIDE

**Ziel**: Kontrollzentrum auf Laptop laden und starten  
**Zeit**: ~2 Minuten  
**Anforderung**: Python 3.8+

---

## 🚀 SCHNELLSTART (Windows)

### Option 1: Batch-Skript (Einfachste Methode)
```bash
START_APP.bat
```

**Das macht das Skript automatisch:**
- ✅ Python prüfen
- ✅ Dependencies installieren
- ✅ App starten

### Option 2: Python direkt
```bash
python INSTALL_AND_RUN.py
```

### Option 3: Manuell
```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. App starten
python PRODUCTION_GO_LIVE.py
```

---

## 📋 VORAUSSETZUNGEN

✅ **Python 3.8+**
```bash
python --version
```

✅ **pip** (Python Package Manager)
```bash
pip --version
```

✅ **Git** (für Submodules)
```bash
git --version
```

---

## 🔧 INSTALLATION SCHRITT FÜR SCHRITT

### Schritt 1: Projekt-Verzeichnis
```bash
cd c:\Users\Laptop\Kontrollzentrum-1
```

### Schritt 2: Dependencies installieren
```bash
pip install -r requirements.txt
```

**Installiert:**
- FastAPI
- uvicorn
- streamlit
- pandas
- numpy
- requests
- ... und weitere

### Schritt 3: App starten
```bash
python PRODUCTION_GO_LIVE.py
```

---

## 🎯 VERWENDUNG

### CLI Mode
```bash
python main.py
```

### Team Mode (Automatisch alle Module)
```bash
python main.py team
```

### API Gateway
```bash
python main.py api
# Öffne: http://localhost:8000
```

### Health Check
```bash
python main.py health
```

---

## 📊 ERWARTET

Nach dem Start siehst du:

```
======================================================================
🚀 KONTROLLZENTRUM - PRODUCTION GO-LIVE
======================================================================

✅ Prüfe Projektstruktur...
✅ Struktur OK

✅ Prüfe Wrapper...
✅ Wrapper OK

✅ Lade Module...
✅ 15+ Module gefunden

======================================================================
🎯 STARTE TEAM-MODUS (Alle Module)
======================================================================

[TEAM-MODUS] Autostart am 01.12.2025 ...
[INSTALLATION] ...
[RUN] ...

======================================================================
✅ PRODUCTION GO-LIVE ERFOLGREICH!
======================================================================

📊 Status:
  ✅ Alle Module geladen
  ✅ Wrapper aktiv
  ✅ Orchestration läuft
  ✅ Log: team_log.txt

🎉 KONTROLLZENTRUM IST LIVE!
```

---

## 🆘 TROUBLESHOOTING

### Problem: Python nicht gefunden
```bash
# Installiere Python von: https://www.python.org
# Wähle: "Add Python to PATH"
```

### Problem: pip nicht gefunden
```bash
python -m pip install -r requirements.txt
```

### Problem: Module nicht gefunden
```bash
# Stelle sicher, dass du im richtigen Verzeichnis bist
cd c:\Users\Laptop\Kontrollzentrum-1
python main.py
```

### Problem: API-Keys fehlen
```bash
# Öffne .env und trage Keys ein
# Siehe: core/key_check.py für erforderliche Keys
```

### Problem: Submodules nicht synchronisiert
```bash
git submodule update --remote --recursive
```

---

## 📁 DATEIEN

| Datei | Zweck |
|-------|-------|
| `START_APP.bat` | Windows Batch-Skript (Einfachste Methode) |
| `INSTALL_AND_RUN.py` | Python Install & Run Skript |
| `PRODUCTION_GO_LIVE.py` | Go-Live Script |
| `main.py` | Entry Point |
| `requirements.txt` | Dependencies |

---

## ✅ FERTIG!

Nach der Installation:

1. **App lädt automatisch**
2. **Alle Module werden geladen**
3. **Team-Modus startet**
4. **Log wird geschrieben** (`team_log.txt`)

---

## 🎯 NÄCHSTE SCHRITTE

1. **App starten**: `START_APP.bat` oder `python INSTALL_AND_RUN.py`
2. **Logs prüfen**: `team_log.txt`
3. **Health-Status**: `python main.py health`
4. **API testen**: `python main.py api`

---

## 📞 SUPPORT

Bei Problemen:
- Siehe `PRODUCTION_README.md`
- Siehe `WRAPPER_QUICKSTART.md`
- Siehe `OPTION_A_ORCHESTRATION.md`

---

*Erstellt: 01.12.2025 | OPTION A Orchestration v1.0*
