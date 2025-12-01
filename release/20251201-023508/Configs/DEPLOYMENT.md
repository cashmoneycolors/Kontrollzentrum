# 🚀 Deployment Guide - Kontrollzentrum

## 1️⃣ VORBEREITUNG

### Schritt 1: Produktive API-Keys eintragen
```bash
# .env öffnen und alle Keys ersetzen
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
STRIPE_API_KEY=sk_live_xxxxxxxxxxxxx
# ... weitere Keys
```

### Schritt 2: Dependencies installieren
```bash
pip install -r requirements.txt
```

### Schritt 3: Tests ausführen
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 2️⃣ LOKALE AUSFÜHRUNG

### Option A: CLI-Modus
```bash
python main.py alle run
```

### Option B: Streamlit-Dashboard
```bash
streamlit run main.py
# Öffnet: http://localhost:8501
```

### Option C: FastAPI-Server
```bash
python modules/ki_sideboard.py
# Öffnet: http://localhost:8003/docs
```

### Option D: Roboter-Modus
```bash
python mega_roboter_ki.py
# Interaktives Menü
```

---

## 3️⃣ WINDOWS BATCH-DATEIEN

### Dashboard starten
```bash
run_dashboard.bat
```

### API-Server starten
```bash
run_api.bat
```

---

## 4️⃣ EXECUTABLE BAUEN (Optional)

### Voraussetzung
```bash
pip install pyinstaller
```

### Build
```bash
.\build_exe.ps1
```

### Output
```
dist/🤖ROBOTER_KI_APP.exe
```

### Verwendung
```bash
# Doppelklick auf .exe oder
.\dist\🤖ROBOTER_KI_APP.exe
```

---

## 5️⃣ AUTOSTART KONFIGURIEREN (Optional)

### Windows Task Scheduler
```bash
.\Kontrollzentrum-Autostart.ps1
```

### Manuell
1. Öffne Task Scheduler
2. Neue Task erstellen
3. Trigger: Bei Anmeldung
4. Aktion: `python main.py team`

---

## 6️⃣ DOCKER DEPLOYMENT (Optional)

### Dockerfile erstellen
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py", "team"]
```

### Build
```bash
docker build -t kontrollzentrum .
```

### Run
```bash
docker run -e OPENAI_API_KEY=sk-... kontrollzentrum
```

---

## 7️⃣ CLOUD DEPLOYMENT (Optional)

### Heroku
```bash
# Procfile erstellen
web: streamlit run main.py

# Deploy
git push heroku main
```

### AWS Lambda
```bash
# Serverless Framework
serverless deploy
```

### Google Cloud Run
```bash
gcloud run deploy kontrollzentrum \
  --source . \
  --platform managed \
  --region us-central1
```

---

## 8️⃣ MONITORING & LOGGING

### Logs anzeigen
```bash
# Team-Modus Log
cat team_log.txt

# Streamlit Logs
# ~/.streamlit/logs/

# FastAPI Logs
# Console-Output
```

### Health-Check
```bash
curl http://localhost:8003/health
```

---

## 9️⃣ BACKUP & RESTORE

### Backup erstellen
```bash
.\backup_kontrollzentrum.ps1
```

### Backup wiederherstellen
```bash
# ZIP extrahieren
Expand-Archive backup_2025-11-30_09-43-11.zip -DestinationPath .
```

---

## 🔟 TROUBLESHOOTING

### Problem: "FEHLENDE API-KEYS"
**Lösung:** Alle Keys in `.env` eintragen
```bash
python -c "from core.key_check import check_all_keys; check_all_keys()"
```

### Problem: "Port bereits in Verwendung"
**Lösung:** Anderen Port verwenden
```bash
streamlit run main.py --server.port 8502
```

### Problem: "Module nicht gefunden"
**Lösung:** Dependencies installieren
```bash
pip install -r requirements.txt
```

### Problem: "Python nicht gefunden"
**Lösung:** Python-Pfad prüfen
```bash
where python
# oder
py --version
```

---

## 📊 DEPLOYMENT-CHECKLISTE

- [ ] API-Keys in `.env` eingetragen
- [ ] Dependencies installiert (`pip install -r requirements.txt`)
- [ ] Tests bestanden (`python -m unittest discover`)
- [ ] CLI-Modus funktioniert (`python main.py alle run`)
- [ ] Dashboard funktioniert (`streamlit run main.py`)
- [ ] API-Server funktioniert (`python modules/ki_sideboard.py`)
- [ ] Backup erstellt (`.\backup_kontrollzentrum.ps1`)
- [ ] Logs überprüft (`cat team_log.txt`)

---

## 🎯 PRODUCTION BEST PRACTICES

### Sicherheit
- ✅ API-Keys in `.env` (nicht im Code)
- ✅ `.env` in `.gitignore`
- ✅ HTTPS für APIs
- ✅ Rate Limiting
- ✅ Input Validation

### Performance
- ✅ Caching aktivieren
- ✅ Async/Await für APIs
- ✅ Connection Pooling
- ✅ Load Balancing

### Monitoring
- ✅ Health Checks
- ✅ Error Logging
- ✅ Performance Metrics
- ✅ Uptime Monitoring

### Backup
- ✅ Tägliche Backups
- ✅ Offsite Storage
- ✅ Restore Tests
- ✅ Disaster Recovery Plan

---

## 1️⃣1️⃣ END-TO-END DEPLOYMENT PIPELINE

### Phase 1: WPF Publish (dotnet)
- Project: `KontrollzentrumDesktop.csproj`, Configuration: `Release`, Runtime: `win-x64`
- Command: `dotnet publish KontrollzentrumDesktop.csproj -c Release -r win-x64 /p:PublishSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true /p:PublishTrimmed=false`
- Output: `bin/Release/net8.0-windows/win-x64/publish/` containing `KontrollzentrumDesktop.exe` plus `appsettings.json`
- Verification: run the published EXE, confirm RestSharp calls hit `http://localhost:8003` while `run_services.ps1` keeps backend alive
- Artifact staging: copy publish folder into `dist/desktop/` for later installer bundling

### Phase 2: Backend Bundle (PyInstaller)
- Pre-req: `pip install -r requirements.txt` and `.env` populated, then run `.
un_services.ps1 -Mode prod` once to verify health
- Build: `.uild_exe.ps1` (wraps `pyinstaller --onefile --name "🤖ROBOTER_KI_APP" main.py`), produces `dist/🤖ROBOTER_KI_APP.exe`
- Supplementary scripts: include `run_services.ps1`, `.env.example`, `requirements.txt`, and `team_log.txt` template for diagnostics
- Artifact staging: move `dist/🤖ROBOTER_KI_APP.exe` + support scripts to `dist/backend/`
- Smoke test: execute the PyInstaller binary, ensure CLI `team` run succeeds and FastAPI endpoints stay reachable

### Phase 3: Installer Assembly
- Structure: `release/` with subfolders `DesktopApp/`, `Backend/`, `Configs/`
- Automation: extend `setup_desktop_app.ps1` to pull artifacts from `dist/desktop` and `dist/backend`, copy `.env.example`, and register `run_services.ps1` as Windows Service (via Task Scheduler) when `-RegisterService` switch supplied
- Optional compression: `Compress-Archive -Path release/* -DestinationPath Kontrollzentrum_Full_{yyyyMMddHHmm}.zip`
- Verification checklist: hash assets, execute installer on clean VM, confirm desktop UI launches + communicates with backend, ensure uninstall removes scheduled tasks/logs
- Publishing: upload the ZIP plus SHA256 file to distribution channel; store release metadata in `FINAL_STATUS.md`

### Operational Handoff
- Document pipeline execution in `PROJECT_STATUS.md` per release cycle
- Tag git commit (`git tag deploy-YYYYMMDD && git push --tags`) after artifacts are archived
- Keep last two releases hot for rollback; archive older zips to cold storage with backups

---

## 📞 SUPPORT

Siehe `QUICKSTART.md` für schnelle Hilfe  
Siehe `DEVELOPER_GUIDE.md` für Modul-Entwicklung  
Siehe `FINAL_STATUS.md` für Projekt-Status

---

**🟢 BEREIT FÜR PRODUKTION**

*Letzte Aktualisierung: 2025-11-30*
