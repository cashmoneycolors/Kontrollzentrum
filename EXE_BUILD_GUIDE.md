# 🚀 ROBOTER_KI_APP.exe - BUILD GUIDE

## Option 1: Batch Launcher (EMPFOHLEN - Schnell & Einfach)

```bash
INSTALL_EXE.bat
```

Das erstellt:
- `ROBOTER_KI_APP.bat` - Batch Launcher
- `ROBOTER_KI_APP.vbs` - VBScript Wrapper
- Beide auf Desktop\Projekte

**Starten:**
```bash
ROBOTER_KI_APP.bat
```

---

## Option 2: Nuitka (Schnell & Kompiliert)

```bash
BUILD_EXE_NUITKA.bat
```

Das erstellt:
- `ROBOTER_KI_APP.exe` - Kompilierte EXE
- Auf Desktop\Projekte

**Starten:**
```bash
ROBOTER_KI_APP.exe
```

---

## Option 3: cx_Freeze (Vollständig)

```bash
pip install cx_Freeze
python setup.py build
```

Das erstellt:
- `build/exe.win-amd64-3.11/ROBOTER_KI_APP.exe`

---

## Option 4: PowerShell Launcher

```powershell
.\ROBOTER_KI_APP.ps1
```

Interaktives Menü im Terminal.

---

## 🎯 Welche Option wählen?

| Option | Größe | Geschwindigkeit | Empfehlung |
|--------|-------|-----------------|-----------|
| Batch | 1 KB | Sofort | ✅ Für schnelle Tests |
| Nuitka | 50-100 MB | Schnell | ✅ Für Produktion |
| cx_Freeze | 100-200 MB | Normal | ⚠️ Komplex |
| PowerShell | 1 KB | Sofort | ✅ Für Entwicklung |

---

## 📋 Menü-Optionen

```
[1] 🚀 Start Team Mode
    → Installiert & startet alle Module automatisch

[2] 🔌 Start API Gateway
    → FastAPI auf http://localhost:8000

[3] 📊 Start Dashboard
    → Streamlit UI auf http://localhost:8501

[4] 🏥 Health Check
    → Prüft System & Module

[5-8] 📋 Run Week 1-4
    → Führt 4-Wochen Execution aus

[9] 🚀 Run All Weeks
    → Komplette Execution (28 Tage)

[0] ❌ Exit
    → Beendet die App
```

---

## ✅ Schnellstart

### Schritt 1: Installation
```bash
INSTALL_EXE.bat
```

### Schritt 2: Starten
```bash
ROBOTER_KI_APP.bat
```

### Schritt 3: Menü wählen
```
Select option: 1
```

---

## 🔧 Troubleshooting

### Problem: "Python not found"
```bash
# Python zu PATH hinzufügen
setx PATH "%PATH%;C:\Python311"
```

### Problem: "Module not found"
```bash
# Dependencies installieren
pip install -r requirements.txt
```

### Problem: "Port already in use"
```bash
# Anderen Port verwenden
python main.py api --port 8001
```

---

## 📦 Dateien

```
ROBOTER_KI_APP.bat          ← Batch Launcher
ROBOTER_KI_APP.ps1         ← PowerShell Launcher
roboter_ki_gui.py          ← GUI Source
setup.py                   ← cx_Freeze Config
BUILD_EXE_NUITKA.bat       ← Nuitka Builder
BUILD_EXE_DIRECT.bat       ← cx_Freeze Builder
INSTALL_EXE.bat            ← Installation
```

---

## 🎉 Fertig!

Deine ROBOTER_KI_APP.exe ist ready!

Starten mit:
```bash
ROBOTER_KI_APP.bat
```

oder

```bash
ROBOTER_KI_APP.exe
```
