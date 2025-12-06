# 🎛️ KONTROLLZENTRUM v5.0 - PRODUCTION OPERATIONS GUIDE

## 🚀 QUICK START (5 Minuten)

### 1. System starten
```bash
python PRODUCTION_START.py
```

### 2. Menü wählen
```
1. 🚀 Team-Modus (alle Module)
2. 🌐 API Gateway
3. 🏥 Health Check
4. 📊 Dashboard
5. 🔧 CLI Mode
6. ❌ Beenden
```

### 3. Monitoring starten
```bash
python PRODUCTION_MONITOR.py
```

---

## 📊 ENTRY POINTS

### Team-Modus (Automatisch)
```bash
python main.py team
```
**Was passiert:**
- ✅ Alle Module werden geladen
- ✅ Installation durchgeführt
- ✅ Ausführung gestartet
- ✅ Logging in team_log.txt
- ✅ Fehlerbehandlung aktiv

**Output:**
```
[TEAM-MODUS] Autostart am 2025-12-01 10:00:00
[INSTALLATION]
Modul: ai_assistant         Status: OK
Modul: data_analytics       Status: OK
...
[RUN]
Modul: ai_assistant         Status: OK
Modul: data_analytics       Status: OK
...
[ZUSAMMENFASSUNG] OK: 25  Demo: 3  Fehler: 0
```

### API Gateway
```bash
python main.py api
```
**Was passiert:**
- ✅ FastAPI Server startet
- ✅ Uvicorn läuft auf Port 8000
- ✅ 50+ REST Endpoints verfügbar
- ✅ Rate Limiting aktiv
- ✅ Caching implementiert

**Zugriff:**
```
http://0.0.0.0:8000
http://0.0.0.0:8000/docs (Swagger UI)
http://0.0.0.0:8000/redoc (ReDoc)
```

### Health Check
```bash
python main.py health
```
**Was passiert:**
- ✅ Module Health Status
- ✅ System Metrics (CPU/Memory/Disk)
- ✅ Alert System
- ✅ Real-time Monitoring

**Output:**
```
🏥 Running health checks...

✅ ai_assistant: healthy (0.05s)
✅ data_analytics: healthy (0.03s)
⚠️  email_automation: slow (0.15s)
...

📊 System Health:
  CPU: 35.2%
  Memory: 42.1%
  Disk: 28.5%
  Status: healthy

⚠️  Alerts (2):
  - CPU usage trending up
  - Memory usage at 42%
```

### CLI Mode
```bash
python main.py
```
**Was passiert:**
- ✅ Interaktive Modul-Auswahl
- ✅ Action-Ausführung
- ✅ Parameter-Support
- ✅ Batch-Operationen

**Beispiele:**
```
> 1 run
> 2 install
> 3 to_svg output.svg
> alle run
```

### Streamlit Dashboard
```bash
streamlit run main.py
```
**Was passiert:**
- ✅ Web UI startet
- ✅ Zenith Controller lädt
- ✅ Real-time Visualisierung
- ✅ Module Management
- ✅ Performance Tracking

**Zugriff:**
```
http://localhost:8501
```

---

## 🔍 MONITORING & TROUBLESHOOTING

### Live Dashboard
```bash
python PRODUCTION_MONITOR.py
```
**Zeigt:**
- 📊 CPU, Memory, Disk in Echtzeit
- 📈 Trends (↑ ↓ →)
- 🚨 Alerts & Warnings
- 🔵 Process Count

### Logs prüfen
```bash
# Team-Modus Logs
tail -f team_log.txt

# System Logs
tail -f logs/kontrollzentrum.log

# Error Logs
tail -f logs/error.log
```

### Database prüfen
```bash
# SQLite öffnen
sqlite3 kontrollzentrum.db

# Tabellen anzeigen
.tables

# User anzeigen
SELECT * FROM users;

# Module Logs anzeigen
SELECT * FROM module_logs ORDER BY timestamp DESC LIMIT 10;
```

### API testen
```bash
# Health Endpoint
curl http://0.0.0.0:8000/health

# Module Status
curl http://0.0.0.0:8000/modules

# Metrics
curl http://0.0.0.0:8000/metrics
```

---

## 🆘 TROUBLESHOOTING

### Problem: Module laden nicht
```bash
# Syntax prüfen
python -m py_compile modules/*.py

# Import testen
python -c "import ai_assistant; print('OK')"

# Logs prüfen
tail -f team_log.txt
```

### Problem: API nicht erreichbar
```bash
# Port prüfen
netstat -an | grep 8000

# Process prüfen
tasklist | grep python

# Firewall prüfen
netsh advfirewall show allprofiles
```

### Problem: Database Fehler
```bash
# Database zurücksetzen
del kontrollzentrum.db

# Neu initialisieren
python main.py team

# Backup wiederherstellen
copy kontrollzentrum.db.backup kontrollzentrum.db
```

### Problem: Memory Leak
```bash
# Monitoring starten
python PRODUCTION_MONITOR.py

# Memory Profiling
python -m memory_profiler main.py

# Prozess beenden
taskkill /PID <pid> /F
```

### Problem: Hohe CPU
```bash
# Top Prozesse anzeigen
tasklist /v | sort /+65

# CPU Profiling
python -m cProfile main.py

# Optimierung durchführen
# - Caching aktivieren
# - Batch Processing
# - Async Operations
```

---

## 📈 PERFORMANCE OPTIMIZATION

### Caching aktivieren
```python
from core.performance import cache_result

@cache_result(ttl=300)
def expensive_operation():
    return result
```

### Batch Processing
```python
# Statt einzelne Requests
for item in items:
    process(item)

# Batch verarbeiten
process_batch(items)
```

### Async Operations
```python
import asyncio

async def async_operation():
    result = await fetch_data()
    return result

asyncio.run(async_operation())
```

### Connection Pooling
```python
# Automatisch in core/database.py
# Konfigurierbar in .env
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

---

## 🔐 SECURITY OPERATIONS

### API Key Management
```bash
# Keys in .env speichern
STRIPE_API_KEY=sk_live_...
PAYPAL_API_KEY=...
NFT_API_KEY=...

# Keys nicht loggen
# Keys nicht in Code hardcoden
# Keys regelmäßig rotieren
```

### User Management
```bash
# Admin User erstellen
python -c "from core.auth import create_user; create_user('admin', 'password', 'admin')"

# User auflisten
sqlite3 kontrollzentrum.db "SELECT * FROM users;"

# User löschen
sqlite3 kontrollzentrum.db "DELETE FROM users WHERE username='user';"
```

### Audit Logging
```bash
# Audit Logs prüfen
sqlite3 kontrollzentrum.db "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 20;"

# Verdächtige Aktivitäten
sqlite3 kontrollzentrum.db "SELECT * FROM audit_logs WHERE action='failed_login';"
```

---

## 📊 METRICS & REPORTING

### System Metrics
```bash
# CPU Usage
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%')"

# Memory Usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Disk Usage
python -c "import psutil; print(f'Disk: {psutil.disk_usage(\"/\").percent}%')"
```

### Module Metrics
```bash
# Module Performance
curl http://0.0.0.0:8000/metrics/modules

# Response Times
curl http://0.0.0.0:8000/metrics/response_times

# Error Rates
curl http://0.0.0.0:8000/metrics/errors
```

### Custom Reports
```bash
# Täglicher Report
python -c "from core.reporting import generate_daily_report; generate_daily_report()"

# Wöchentlicher Report
python -c "from core.reporting import generate_weekly_report; generate_weekly_report()"

# Monatlicher Report
python -c "from core.reporting import generate_monthly_report; generate_monthly_report()"
```

---

## 🔄 MAINTENANCE TASKS

### Tägliche Tasks
- [ ] Health Check durchführen
- [ ] Logs prüfen
- [ ] Alerts überprüfen
- [ ] Performance Baseline prüfen
- [ ] Backup durchführen

### Wöchentliche Tasks
- [ ] Database Optimization
- [ ] Log Rotation
- [ ] Security Scan
- [ ] Performance Report
- [ ] Capacity Planning

### Monatliche Tasks
- [ ] Full Backup
- [ ] Disaster Recovery Test
- [ ] Security Audit
- [ ] Performance Tuning
- [ ] Documentation Update

---

## 🚨 INCIDENT RESPONSE

### Kritischer Alert
```bash
# 1. Monitoring starten
python PRODUCTION_MONITOR.py

# 2. Logs prüfen
tail -f team_log.txt

# 3. Health Check
python main.py health

# 4. Betroffene Module identifizieren
curl http://0.0.0.0:8000/modules

# 5. Notfalls neustarten
python main.py team
```

### Rollback Procedure
```bash
# 1. Backup wiederherstellen
copy kontrollzentrum.db.backup kontrollzentrum.db

# 2. System neustarten
python main.py team

# 3. Health Check
python main.py health

# 4. Monitoring
python PRODUCTION_MONITOR.py
```

---

## 📞 SUPPORT & RESOURCES

### Dokumentation
- README.md - Überblick
- PRODUCTION_STATUS.md - Status
- PRODUCTION_CHECKLIST.md - Checkliste
- API_DOCUMENTATION.md - API Docs

### Logs & Debugging
- team_log.txt - Team-Modus Logs
- logs/kontrollzentrum.log - System Logs
- logs/error.log - Error Logs
- kontrollzentrum.db - Database

### Tools
- PRODUCTION_START.py - Launcher
- PRODUCTION_MONITOR.py - Monitor
- PRODUCTION_DEPLOY.bat - Deployment
- main.py - Main Entry Point

---

**🎉 Kontrollzentrum v5.0 ist produktionsreif!**

**Starten Sie mit:** `python PRODUCTION_START.py`
