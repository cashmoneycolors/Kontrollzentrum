
# 🤖 Copilot-Instructions für Kontrollzentrum (QUANTUM AUTONOMOUS MODE)

## 🎯 Architektur-Prinzipien (Zero-Compromise Design)

**🔌 Plug-and-Play-Modularchitektur:** Jedes Modul in `modules/` implementiert eine `run()`-Funktion. Module werden automatisch erkannt, geladen und registriert - KEINE manuelle Konfiguration erforderlich.

**🔐 Zero-Tolerance Key-Policy (KRITISCH):** Der `@require_keys`-Decorator aus `core/key_check.py` verhindert jeden Start ohne vollständige `.env`-Konfiguration. **KEIN Demo-Modus, KEINE Fallbacks, KEINE Platzhalter!**

```python
REQUIRED_KEYS = [
    "OPENAI_API_KEY", "STRIPE_API_KEY", "PAYPAL_CLIENT_ID",
    "PAYPAL_CLIENT_SECRET", "EBAY_APP_ID", "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY", "NFT_API_KEY", "SMTP_USER", "SMTP_PASSWORD"
]
```

**⚡ Zenith Controller (System Core):** `core/zenith_controller.py` orchestriert das gesamte System mit:
- Streamlit-UI (Multi-Module-Dashboard)
- System-Recovery (`self.recover()`) - Automatische Fehlerbehebung
- Performance-Monitoring (`self.monitor_performance()`) - Echtzeit-Metriken
- Policy-Enforcement (`self.enforce_policy()`) - Regelbasierte Governance
- Audit-Trail (`self.audit()`) - Vollständige Nachverfolgbarkeit

## 🚀 Kritische Workflows (Production-Ready)

### 🏁 Projekt-Start (3 Modi)

**1️⃣ AUTONOMER ROBOTER-MODUS (Vollautomatik):**
```powershell
python mega_roboter_ki.py
# Interaktives Menü:
# 1. Struktur prüfen/anlegen
# 2. Abhängigkeiten auto-installieren
# 3. Alle Module testen
# 4. API-Integration testen
# 5. Backup erstellen
```

### 🧩 Modul-Entwicklung (Production Pattern)

**Standard-Modul-Template:**
```python
# modules/neues_modul.py
from core.key_check import require_keys
import os
from dotenv import load_dotenv

load_dotenv()

@require_keys  # STOPPT Ausführung wenn Keys fehlen!
def run(*args):
    """Modul-Hauptlogik - läuft NUR mit vollständigen Keys"""
    api_key = os.getenv("REQUIRED_KEY")
    # Produktive Logik hier
    return {"status": "success", "data": result}

def install():
    """Optional: Installations-Routine"""
    print("Installing dependencies...")
    # pip install, Setup-Schritte

def describe():
    """Optional: Modul-Beschreibung für Discovery"""
    return "Modulname - Kurzbeschreibung der Funktionalität"
```

**FastAPI-Modul-Template:**
### 📦 Build & Deployment (Production Distribution)

**🏗️ Executable Build (PyInstaller):**
```powershell
# Automatischer Build mit Dependencies
.\build_exe.ps1

# Manueller Build (alternativ)
pip install pyinstaller
pyinstaller --onefile --name "🤖ROBOTER_KI_APP" mega_roboter_ki.py

# Output: dist/🤖ROBOTER_KI_APP.exe
## 💎 Projekt-spezifische Konventionen (Quantum Standards)

### 🎭 Multi-Entry-Point-Architektur (3 Hauptmodi)

| Entry-Point | Zweck | Verwendung |
|------------|-------|------------|
| **`main.py`** | CLI + Streamlit Dashboard | `python main.py` oder `streamlit run main.py` |
| **`mega_roboter_ki.py`** | Autonomer Setup/Test/Backup | `python mega_roboter_ki.py` (interaktiv) |
| **Module direkt** | API-Server einzeln starten | `python modules/ki_sideboard.py` |

### 🤖 Team-Modus (Vollautomatische Orchestrierung)

```powershell
python main.py team
# Führt automatisch aus:
# 1. Alle Module mit install() - Installation
# 2. Alle Module mit run() - Ausführung
# 3. Schreibt team_log.txt mit:
#    - Installations-Status (OK/FEHLER/DEMO)
#    - Run-Status mit Zeitstempeln
#    - Zusammenfassung: Erfolge/Fehler/Demo-Modi
```

**Log-Format:**
```
[TEAM-MODUS] Autostart am 2025-11-28 12:00:00

[INSTALLATION]
Modul: data_import         Status: OK
Modul: nft_modul          Status: FEHLER (Missing NFT_API_KEY)
[ZUSAMMENFASSUNG] Erfolgreich: 8  Fehlgeschlagen: 2

[RUN]
Modul: data_import         Status: OK
Modul: ki_modul           Status: DEMO-MODUS (OpenAI key missing)
[ZUSAMMENFASSUNG] OK: 6  Demo: 2  Fehler: 2
```

### 🎮 CLI-Pattern (Batch-Operationen)

```powershell
# Syntax: python main.py [modul|alle|team] [aktion] [args...]

# Alle Module mit Aktion
python main.py alle install        # Installiert alle Module
python main.py alle run           # Führt alle Module aus

# Spezifisches Modul (nach Nummer aus Discovery-Liste)
python main.py 1 run              # Startet Modul #1
python main.py 3 to_svg out.svg   # Modul #3 SVG-Export
python main.py 5 describe         # Modul #5 Beschreibung

# Team-Modus (keine weitere Eingabe nötig)
python main.py team               # Vollautomatik
```

### 🚫 Zero-Tolerance-Policy (KRITISCH!)

**ABSOLUT VERBOTEN:**
- ❌ Demo-Modi wenn Keys fehlen
- ❌ Placeholder-Values (`"your-key-here"`)
- ❌ Fallback auf lokale/Mock-Daten
- ❌ Stille Key-Fehler (logs only)
- ❌ Partial Funktionalität

**PFLICHT:**
- ✅ Sofortiger Abbruch bei fehlendem Key
- ✅ Klare Fehlermeldung mit Key-Name
- ✅ `@require_keys` auf ALLEN produktiven Funktionen
- ✅ Key-Check im `__main__` und API-Startup
- ✅ Komplette Funktionalität oder gar nicht

```python
# ✅ RICHTIG
@require_keys
def process():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY fehlt in .env!")
    # Produktive Logik

# ❌ FALSCH
def process():
    api_key = os.getenv("API_KEY", "demo-key")  # VERBOTEN!
    if not api_key:
        return {"demo": True}  # VERBOTEN!
```
    # Produktive API-Logik
    return {"result": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
```

**Auto-Discovery-Mechanismus:** 
- `main.py` scannt `modules/*.py` automatisch
- Erkennt Capabilities: `run`, `install`, `to_svg`, `to_word`, `describe`
- KEINE manuelle Registrierung erforderlich
- Module erscheinen automatisch in CLI + UI

# Spezifisches Modul
python main.py 2 run param1 param2

# Alle Module mit Aktion
python main.py alle install
```
## ⚡ VS Code Productivity Tips (Quantum Efficiency)

### 🎯 Multicursor (Batch-Edits @ Light-Speed)
```
Alt+Click             → Cursor hinzufügen (beliebige Position)
Ctrl+Alt+Down/Up      → Cursor vertikal stapeln
Ctrl+D                → Nächstes Vorkommen selektieren (Kette)
Ctrl+K Ctrl+D         → Vorkommen überspringen (bei Ctrl+D)
Ctrl+Shift+L          → ALLE Vorkommen selektieren (Masse-Edit)
Shift+Alt+Right/Left  → Auswahl intelligent erweitern/verkleinern
Shift+Alt+I           → Cursor an Zeilenenden aller Zeilen
```

**Praxis-Beispiel (API-Keys bulk-updaten):**
1. `Ctrl+D` auf erstem `os.getenv("KEY")`
2. Mehrmals `Ctrl+D` für alle Matches
3. `Shift+Alt+Right` um String zu erweitern
4. Tippen zum simultanen Ersetzen

### 🔍 Suchen & Ersetzen (Regex Power-Mode)
```
Ctrl+F                → In Datei suchen
## 🛡️ Recovery & Debugging (Self-Healing System)

### 🔄 System Recovery (Automatische Wiederherstellung)

**Via UI (Zenith Controller):**
```python
# Sidebar-Button triggert:
controller.recover()
# Führt aus:
# 1. Service-Health-Checks
# 2. Restart fehlgeschlagener Module
# 3. Cache-Clearing
# 4. Connection-Pool-Reset
```

**Via CLI (Mega Roboter KI):**
```powershell
python mega_roboter_ki.py
# Option 3: Module testen (mit Auto-Recovery)
# Option 4: API-Integration testen
```

### 🔑 Key-Fehler beheben (Systematischer Fix)

**1. Fehlerdiagnose:**
```powershell
# Zeigt ALLE fehlenden Keys
python -c "from core.key_check import check_all_keys; check_all_keys()"

# Output:
# ============================================================
# FEHLENDE API-KEYS!
# Die folgenden Keys fehlen in deiner .env-Datei:
# - OPENAI_API_KEY
# - STRIPE_API_KEY
# Bitte trage alle Keys in die .env ein und starte neu.
# ============================================================
```

**2. Keys nachtragen:**
```bash
# .env öffnen und ALLE fehlenden Keys ergänzen
# Format: KEY=value (KEINE Anführungszeichen!)

OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
STRIPE_API_KEY=sk_live_xxxxxxxxxxxxx
```

**3. Validierung:**
```powershell
# Erneut prüfen
python -c "from core.key_check import check_all_keys; check_all_keys()"
# Kein Output = Alle Keys vorhanden ✅

# App starten
python main.py
```

### 🐛 Module debuggen (Isolation & Tracing)

**Einzelmodul-Test:**
```powershell
# Methode 1: Direkter Import
python -c "from modules.modulname import run; run()"

# Methode 2: Als Package
python -m modules.modulname

# Methode 3: Main-Check aktivieren
python modules/modulname.py
```

**API-Modul debuggen:**
```powershell
# 1. Starte API-Server
python modules/ki_sideboard.py
# Server läuft auf http://localhost:8003

# 2. Health-Check
curl http://localhost:8003/health

# 3. Endpunkt testen (Postman/curl)
curl -X POST http://localhost:8003/openai_vision \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/img.jpg"}'

# 4. Logs beachten (Console-Output)
```

**Verbose-Logging aktivieren:**
```python
# In Modul einfügen (temporär):
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 📊 Team-Log analysieren (Post-Mortem)

```powershell
# Nach Team-Modus Durchlauf
cat team_log.txt

# Oder: Gefiltert nach Fehlern
Select-String -Path team_log.txt -Pattern "FEHLER|ERROR"

# Log-Struktur:
# [TIMESTAMP] [PHASE] Modul: NAME  Status: OK/FEHLER/DEMO-MODUS
# [ZUSAMMENFASSUNG] Erfolge/Fehler-Count
```

**Typische Fehlerquellen:**
| Fehlermeldung | Ursache | Fix |
|--------------|---------|-----|
| `Missing KEY_NAME` | Key fehlt in .env | Key in .env ergänzen |
| `ModuleNotFoundError` | Dependency fehlt | `pip install package` |
| `HTTPException 500` | API-Key ungültig | Key-Validity prüfen |
| `Connection refused` | Service nicht erreichbar | Service-Status checken |

### 🧪 Debugging-Checkliste (Systematisch)

- [ ] **Keys validieren:** `check_all_keys()` erfolgreich?
- [ ] **Dependencies:** `pip list` zeigt alle Packages?
- [ ] **Imports:** Modul lädt ohne ImportError?
- [ ] **Einzeltest:** `python modules/modul.py` funktioniert?
- [ ] **Logs:** Fehlermeldungen in Console/team_log.txt?
- [ ] **API-Health:** Endpoints erreichbar (curl/Postman)?
- [ ] **.env-Format:** Keine Quotes, keine Spaces um `=`?
- [ ] **Python-Version:** `python --version` >= 3.8?

---
*Stand: November 2025 | Branch: blackboxai/azure-mcp-setup | Quantum-Optimiert für autonome AI-Agents*
```

### 🧭 Navigation (Zero-Friction Flow)
```
F12                  → Zur Definition (same editor)
Ctrl+K F12           → Definition in Side-Editor
Alt+F12              → Peek Definition (Inline-Popup)
Ctrl+Shift+O         → Symbole in Datei (Quick-Jump)
Ctrl+T               → Symbole im Workspace (Global)
Ctrl+P               → Datei öffnen (Fuzzy-Search)
Ctrl+G               → Zu Zeile springen
Ctrl+Shift+\         → Zur passenden Klammer
Alt+Left/Right       → Navigation-History vor/zurück
```

### 🚀 Advanced Productivity Hacks
```
Ctrl+K Ctrl+0        → Alle Regionen falten
Ctrl+K Ctrl+J        → Alle Regionen entfalten
Ctrl+K Ctrl+C        → Zeilen kommentieren
Ctrl+K Ctrl+U        → Zeilen entkommentieren
Alt+Up/Down          → Zeile verschieben
Shift+Alt+Up/Down    → Zeile duplizieren
Ctrl+Shift+K         → Zeile löschen
Ctrl+Enter           → Zeile darunter einfügen
Ctrl+Shift+Enter     → Zeile darüber einfügen
```

**Column Selection (Box-Mode):**
```
Shift+Alt+Maus-Drag  → Spalten-Auswahl (Box)
Shift+Alt+Ctrl+↓/↑   → Spalten-Cursor erweitern
```
@require_keys  # Prüft ALLE REQUIRED_KEYS automatisch
def run():
    """Modul-Hauptlogik - wird nur ausgeführt wenn alle Keys vorhanden"""
    print("Modul läuft produktiv!")
    return result
```

**Module-Discovery:** `main.py` scannt automatisch `modules/` nach `.py`-Dateien und lädt alle Capabilities (`run`, `install`, `to_svg`, `to_word`, `describe`).

### 🧪 Testing-Strategien (Test-Driven Quality Assurance)

**Test-Pyramid (Bottom-Up):**
```powershell
# LEVEL 1: Unit-Tests (Einzelne Funktionen)
python -m unittest tests/test_new_modules.py
# Testet: run(), install(), describe() pro Modul

# LEVEL 2: Integration-Tests (Modul-Interaktionen)
python -m unittest tests/test_all_productive_modules.py
# Testet: data_import → kpi_dashboard → agent_simulator

# LEVEL 3: System-Tests (End-to-End)
python test_runner.py
# Orchestriert alle Tests + Performance-Benchmarks

# LEVEL 4: Acceptance-Tests (Produktions-Simulation)
python main.py team
# Voller Durchlauf mit Logging → team_log.txt analysieren
```

**Test-Execution-Matrix:**
```powershell
# Alle Tests discovern (automatisch)
python -m unittest discover

# Spezifische Test-Klasse
python -m unittest tests.test_new_modules.TestKIIntegrationModul

# Einzelner Test
python -m unittest tests.test_new_modules.TestKIIntegrationModul.test_run

# Mit Verbose-Output
python -m unittest discover -v

# Mit Coverage (wenn installiert)
pip install coverage
coverage run -m unittest discover
coverage report -m
```

**Custom Test-Runner (`test_runner.py`):**
```python
# Erweiterte Features:
# - Performance-Benchmarking
# - Parallel-Test-Execution
# - HTML-Reports
# - CI/CD-Integration (Exit-Codes)

python test_runner.py --parallel --html-report
```

### Build & Deployment
```powershell
# Executable mit PyInstaller erstellen
.\build_exe.ps1

# Backup erstellen (ohne Secrets!)
.\backup_kontrollzentrum.ps1

# Autostart konfigurieren
.\Kontrollzentrum-Autostart.ps1
```

## Projekt-spezifische Konventionen

**Multi-Entry-Point-Architektur:**
- `main.py`: CLI + Streamlit Zenith Controller (Haupteinstieg)
- `mega_roboter_ki.py`: Autonomer Roboter-Modus (volle Automatisierung)
- Module können einzeln gestartet werden für API-Server

**Team-Modus (Vollautomatik):**
```powershell
# Alle Module installieren UND ausführen mit Logging
python main.py team
```
Erstellt `team_log.txt` mit detaillierten Ausführungsprotokollen für alle Module.

**CLI-Pattern:**
```powershell
# Alle Module installieren
python main.py alle install

# Spezifisches Modul mit Aktion
python main.py 2 to_svg output.svg

# Modul mit Parametern
python main.py 3 run param1 param2
```

**FastAPI-Integration:** Module wie `ki_sideboard.py` bieten HTTP-APIs. Pattern:
```python
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.post("/endpoint")
async def handler():
    api_key = os.getenv("SERVICE_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="SERVICE_KEY fehlt in .env")
    # Produktive Logik
```

**Keine Defaults, keine Fallbacks:** Module ohne vollständige API-Keys dürfen niemals starten oder Demo-Modi anbieten. System-Integrität > Benutzerfreundlichkeit.

## 🎛️ Zenith Controller Integration (Orchestrierungs-Layer)

### 📡 Sidebar-Module (UI-Dashboard-Komponenten)

```python
# Vollständige Module-Liste mit Funktions-Signatur:

# 1. DATA PIPELINE
data_import.run()                    # → dict: Importierte Daten
kpi_dashboard.run(data: dict)        # Visualisiert KPIs aus data

# 2. AI/ML LAYER  
agent_simulator.run(data: dict)      # Simuliert Multi-Agenten-System
trailer_visualization.run(data: dict) # Video/Media-Preview-Rendering

# 3. SYSTEM CORE
self_heal.show_live_status()         # → dict: CPU/RAM/Disk-Metriken
controller.recover()                 # Automatische System-Recovery

# 4. BUSINESS LOGIC
payment.check_license(user_id: str)  # Lizenz-Validierung
payment.process_payment(amount, method, email)  # Stripe/PayPal-Integration

# 5. NFT & BLOCKCHAIN
nft_manager.create_nft(image_path, metadata: dict)  # NFT-Minting
nft_manager.list_on_opensea(nft_id)  # OpenSea-Listing

# 6. DISTRIBUTION
auto_distribute.upload_to_ebay(file, title, desc)    # eBay-Upload
auto_distribute.upload_to_amazon(file, metadata)     # Amazon-Upload

# 7. SECURITY
apikey_manager.generate_api_key()    # Neue API-Keys generieren
apikey_manager.encrypt_key(key)      # Key-Verschlüsselung
```

### 🎮 Controller-Methoden (Self-Correcting System Core)

```python
controller = ZenithController()

# MONITORING & METRICS
controller.monitor_performance(cpu_usage: float)
# Trackt CPU-Auslastung, triggert Alerts bei >95%
# Schreibt Metriken in time-series DB

# AUDIT TRAIL
controller.audit(action: str)
# Vollständige Nachverfolgbarkeit aller Systemaktionen
# Format: [TIMESTAMP] [USER] [ACTION] [DETAILS]

# POLICY ENFORCEMENT
controller.enforce_policy(rule: str, condition: bool)
# Regelbasierte Governance
# Beispiel: enforce_policy("KPI-Grenzwert", cpu < 0.95)
# Triggert Actions bei Policy-Violations

# SYSTEM RECOVERY
controller.recover()
# Automatische Wiederherstellung bei Fehlern:
# 1. Health-Checks aller Services
# 2. Restart fehlgeschlagener Module
# 3. Cache/Connection-Reset
# 4. Rollback bei Critical Failures
```

### 🔧 Integration-Pattern (Neue Module in UI einbinden)

**Schritt 1: Modul in `modules/` erstellen**
```python
# modules/neues_feature.py
from core.key_check import require_keys

@require_keys
def run(data=None):
    """Feature-Hauptlogik"""
    return {"result": "success"}
```

**Schritt 2: In Zenith Controller registrieren**
```python
# core/zenith_controller.py - run() Methode erweitern:

def run(self):
    menu = st.sidebar.radio("Modul wählen:", [
        # ...bestehende Module...
        "🆕 Neues Feature"  # Hinzufügen
    ])
    
    # ...bestehende if-Blöcke...
    
    elif menu == "🆕 Neues Feature":
        st.header("🆕 Neues Feature")
        if st.button("Feature starten"):
            result = neues_feature.run(self.data)
            st.json(result)
            self.audit("Neues Feature gestartet")
```

**Schritt 3: Auto-Discovery nutzen (CLI)**
```python
# KEIN Code nötig! main.py findet Module automatisch:
# python main.py  # Zeigt alle Module inkl. neues_feature
# python main.py 10 run  # Startet neues Feature
```

## 📦 Externe Abhängigkeiten (Production Stack)

### 🔧 Core Framework (Minimal Required)
```toml
streamlit         # UI-Dashboard (Zenith Controller)
fastapi           # REST API-Layer (Module wie ki_sideboard)
uvicorn           # ASGI Server für FastAPI
python-dotenv     # Environment-Management (.env loading)
requests          # HTTP-Client (externe API-Calls)
```

### 🤖 AI/ML Services (Keys erforderlich!)
```python
# OpenAI GPT-4, DALL-E, Whisper
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
## 📁 Wichtige Dateipfade (Projekt-Navigator)

### 🎯 Core-Infrastruktur (System-Kern)
```
core/
├── zenith_controller.py              # Haupt-Controller (Streamlit UI + Orchestrierung)
├── zenith_controller_blueprint.py    # Abstract Base Class (Blueprint für Extensions)
└── key_check.py                      # Key-Validation (REQUIRED_KEYS + @require_keys)
```

**Funktionen:**
- `ZenithController`: Streamlit-Dashboard mit Multi-Modul-Sidebar
- `ZenithControllerBlueprint`: Interface für neue Controller-Implementierungen
- `check_all_keys()`: Validiert ALLE REQUIRED_KEYS, wirft RuntimeError
- `@require_keys`: Decorator für Funktionen (stoppt bei fehlenden Keys)

### 🚪 Entry-Points (Startmodi)
```
main.py                   # CLI + Streamlit (python main.py [team|alle|modul])
mega_roboter_ki.py        # Autonomer Setup/Test/Backup-Wizard (interaktiv)
modules/*.py              # Direkte API-Server-Starts (python modules/ki_sideboard.py)
```

**Verwendung:**
- `main.py`: Standard-Einstieg für Entwicklung + Produktion
- `mega_roboter_ki.py`: First-Time-Setup, Testing, Maintenance
- Module direkt: API-Entwicklung, Debugging einzelner Services

### 🏗️ Build & Deploy (Distribution-Pipeline)
```
build_exe.ps1                     # PyInstaller-Build → 🤖ROBOTER_KI_APP.exe
backup_kontrollzentrum.ps1        # Backup-Skript (excludes .env!)
Kontrollzentrum-Autostart.ps1     # Windows Task Scheduler Setup
🤖ROBOTER_KI_APP.spec            # PyInstaller Config (main build)
mega_roboter_ki.spec              # PyInstaller Config (roboter build)
```

**Build-Output:**
```
dist/
└── 🤖ROBOTER_KI_APP.exe        # Standalone Executable (keine Python nötig!)

Ziel: C:\Users\Laptop\Desktop\Projekte\MEGA ULTRA ROBOTER KI\
```

### 📚 Dokumentation (Knowledge Base)
```
README.md                         # Projekt-Overview + Quick-Start
MEGA_WORKFLOW_CHECKLISTE.md       # Team-Workflow-Guide (7-Schritte-Prozess)
.github/copilot-instructions.md   # Diese Datei (AI-Agent-Instructions)
backup_README.md                  # Backup/Restore-Anleitung
```

**Wichtigste Docs für Onboarding:**
1. `README.md` → Verstehen was das Projekt macht
2. `MEGA_WORKFLOW_CHECKLISTE.md` → Entwicklungs-Workflow lernen
3. `.github/copilot-instructions.md` → AI-Agent optimal nutzen

### 🧪 Testing-Infrastruktur
```
tests/
├── test_all_productive_modules.py   # Tests für Core-Business-Module
├── test_new_modules.py              # Tests für neue/experimentelle Module
├── test_nft_modul.py                # Spezifischer NFT-Module-Test
└── test_runner.py                   # Custom Test-Runner (orchestriert alle Tests)
```

**Test-Execution:**
```powershell
python -m unittest tests/test_all_productive_modules.py  # Core-Module
python -m unittest discover                              # Alle Tests
python test_runner.py                                    # Custom-Runner
```

### 🔒 Secrets & Configuration (NIEMALS committen!)
```
.env                # ALLE API-Keys (siehe REQUIRED_KEYS in key_check.py)
.env.example        # Template (Platzhalter, commitbar)
```

**Kritisch:**
- `.env` ist in `.gitignore` → Check mit `git status` (darf NICHT staged sein!)
- Nach Clone: `.env.example` → `.env` kopieren und Keys eintragen
- Alle 10 REQUIRED_KEYS müssen gesetzt sein (sonst: RuntimeError)

### 🧩 Modules-Verzeichnis (Plug-and-Play)
```
modules/
├── [leer aktuell - Module werden dynamisch hinzugefügt]
└── README.md (optional - Modul-Dokumentation)

Erwartete Struktur (nach Entwicklung):
modules/
├── data_import.py           # Daten-Pipeline
├── kpi_dashboard.py         # KPI-Visualisierung
├── agent_simulator.py       # Multi-Agenten-Simulation
├── ki_sideboard.py          # FastAPI KI-Services (/openai_vision, /mathpix)
├── payment.py               # Stripe/PayPal-Integration
├── nft_manager.py           # NFT-Minting/OpenSea-Listing
├── auto_distribute.py       # eBay/Amazon-Upload
└── apikey_manager.py        # Key-Generierung/Verschlüsselung
```

**Auto-Discovery:** `main.py` scannt `modules/*.py` automatisch → CLI + Team-Modus

### 🗑️ Ignorierte Verzeichnisse (Build-Artefakte)
```
__pycache__/        # Python Bytecode (auto-generiert)
dist/               # PyInstaller Output (Executables)
build/              # PyInstaller Build-Cache
*.pyc               # Compiled Python Files
.pytest_cache/      # Pytest Runtime-Daten
```

**Cleanup:**
```powershell
# Alle Build-Artefakte löschen
Remove-Item -Recurse -Force __pycache__, dist, build, .pytest_cache
```

---

## 🎓 Quick-Reference-Karte (Cheat-Sheet für Agents)

```
📍 Projekt starten       → python main.py  (oder: streamlit run main.py)
🤖 Autonomer Modus       → python mega_roboter_ki.py
🔑 Keys prüfen          → python -c "from core.key_check import check_all_keys; check_all_keys()"
🧪 Tests ausführen      → python -m unittest discover
🏗️ Build Exe            → .\build_exe.ps1
💾 Backup erstellen      → .\backup_kontrollzentrum.ps1
📊 Team-Modus           → python main.py team
🔍 Modul debuggen       → python modules/modulname.py
🌐 API starten          → python modules/ki_sideboard.py
📝 Logs analysieren     → cat team_log.txt
```

---
*Stand: November 2025 | Branch: blackboxai/azure-mcp-setup | QUANTUM-OPTIMIERT für autonome AI-Agents 🚀*

### ☁️ Cloud & Infrastructure (Keys erforderlich!)
```python
# AWS S3, EC2, Lambda
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
AWS_REGION=eu-central-1
# Verwendung: modules/auto_distribute.py (S3-Storage)

# SMTP E-Mail (Notifications)
SMTP_USER=noreply@kontrollzentrum.com
SMTP_PASSWORD=xxxxxxxxxxxxx
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
# Verwendung: modules/notification.py (E-Mail-Versand)
```

### 🖼️ NFT & Blockchain (Keys erforderlich!)
```python
# NFT API (OpenSea, Rarible Integration)
NFT_API_KEY=xxxxxxxxxxxxx
NFT_WALLET_ADDRESS=0xxxxxxxxxxxxx
NFT_PRIVATE_KEY=xxxxxxxxxxxxx  # NIEMALS committen!
# Verwendung: modules/nft_manager.py (NFT-Minting/Listing)
```

### 📊 Optional Dependencies (Feature-abhängig)
```python
# Data Science Stack (wenn Data-Module genutzt)
pandas            # DataFrames (data_import, kpi_dashboard)
numpy             # Numerische Operationen
matplotlib        # Plotting (kpi_dashboard)

# Database Connectors (wenn DB-Anbindung)
sqlalchemy        # ORM für PostgreSQL/MySQL
pymongo           # MongoDB-Client

# Testing Framework
pytest            # Unit-Tests (tests/)
pytest-asyncio    # Async-Tests (FastAPI-Module)
```

### 🚀 Installation (One-Command Setup)
```powershell
# Alle Core + Optional Dependencies
pip install -r requirements.txt

# Oder: Nur Core (Minimal)
pip install streamlit fastapi uvicorn python-dotenv requests
```

### 🔐 Security Best Practices (Keys Management)

**✅ DO:**
- Keys in `.env` speichern (root-level)
- `.env` in `.gitignore` (NIEMALS committen!)
- Encrypted Keys via `apikey_manager.encrypt_key()`
- Rotation-Policy: Keys alle 90 Tage wechseln
- Separate Keys für Dev/Staging/Prod

**❌ DON'T:**
- Keys hardcoden in Python-Files
- Keys in Logs/Fehlermeldungen ausgeben
- Keys in Git-History (auch nicht alte Commits!)
- Shared Keys zwischen Services
- Keys in Umgebungsvariablen (Server-Level)

## Wichtige Dateipfade

**Core-Infrastruktur:**
- `core/zenith_controller.py` - Haupt-Controller mit Streamlit-UI
- `core/zenith_controller_blueprint.py` - Abstract Base Class
- `core/key_check.py` - Key-Validation (`REQUIRED_KEYS`, `@require_keys`)

**Entry-Points:**
- `main.py` - CLI + Streamlit (Discovery, Team-Modus)
- `mega_roboter_ki.py` - Autonomer Roboter-Modus

**Build & Deploy:**
- `build_exe.ps1` - PyInstaller Build
- `backup_kontrollzentrum.ps1` - Backup-Skript
- `Kontrollzentrum-Autostart.ps1` - Autostart-Konfiguration
- `🤖ROBOTER_KI_APP.spec`, `mega_roboter_ki.spec` - PyInstaller Specs

**Dokumentation:**
- `MEGA_WORKFLOW_CHECKLISTE.md` - Team-Workflow-Guide
- `README.md` - Projekt-Übersicht
- `.github/copilot-instructions.md` - Diese Datei

**NIEMALS committen:**
- `.env` - Enthält ALLE produktiven API-Keys

## VS Code Productivity Tips

**Multicursor (schnelle Batch-Edits):**
- `Alt+Click` - Cursor hinzufügen
- `Ctrl+Alt+Down/Up` - Cursor vertikal hinzufügen
- `Ctrl+D` - Nächstes Vorkommen selektieren
- `Ctrl+Shift+L` - Alle Vorkommen selektieren
- `Shift+Alt+Right/Left` - Auswahl erweitern/verkleinern

**Suchen & Ersetzen:**
- `Ctrl+F` - In Datei suchen
- `Ctrl+Shift+F` - In allen Dateien suchen
- `Ctrl+H` - Ersetzen
- `Alt+L` - "Find in Selection" toggle
- Regex-Support mit Case-Modifikatoren: `\u`, `\U`, `\l`, `\L`

**Navigation:**
- `F12` - Zur Definition
- `Ctrl+K F12` - Definition in Seiteneditor
- `Ctrl+Shift+O` - Symbole in Datei
- `Ctrl+P` - Datei öffnen

## Recovery & Debugging

**System Recovery:** Sidebar-Button "System Recovery auslösen" triggert `zenith_controller.recover()` für automatische Systemwiederherstellung.

**Key-Fehler beheben:**
1. Fehlerausgabe zeigt fehlende Keys
2. `.env` öffnen und Keys ergänzen
3. App neu starten - keine Teillösungen möglich

**Module debuggen:**
1. Einzeln starten: `python -m modules.modulname`
2. Logs prüfen (stdout/stderr)
3. `.env` validieren mit `python -c "from core.key_check import check_all_keys; check_all_keys()"`

**Team-Log analysieren:**
```powershell
# Nach Team-Modus Run
cat team_log.txt
```
Zeigt Installation und Run-Status aller Module.

---
*Stand: November 2025 | Branch: blackboxai/azure-mcp-setup*
