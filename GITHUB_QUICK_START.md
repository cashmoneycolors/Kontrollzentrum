# 🚀 GitHub Quick Start

## Option 1: Automatisch (Empfohlen)

### Windows CMD:
```bash
PUSH_TO_GITHUB.bat
```

### PowerShell:
```powershell
.\PUSH_TO_GITHUB.ps1
```

## Option 2: Manuell

### 1. GitHub Token erstellen
- Gehe zu: https://github.com/settings/tokens
- Klick "Generate new token (classic)"
- Wähle "repo" Berechtigung
- Kopiere den Token

### 2. Repository auf GitHub erstellen
- Gehe zu: https://github.com/new
- Name: `kontrollzentrum`
- Beschreibung: `Kontrollzentrum v5.0 - Production Grade System`
- Public oder Private
- Klick "Create repository"

### 3. Lokal pushen
```bash
git remote add origin https://TOKEN@github.com/USERNAME/kontrollzentrum.git
git branch -M main
git push -u origin main
```

## ✅ Fertig!

Dein Projekt ist jetzt auf GitHub:
- https://github.com/USERNAME/kontrollzentrum
- Automatische Tests laufen bei jedem Push
- Docker Image wird gebaut
- Deployment ready!

## 📊 Was wird gepusht?

✅ Alle Python-Module (30+)
✅ Core-Systeme (API, Monitoring, DB)
✅ Tests & Dokumentation
✅ Docker & Kubernetes Config
✅ GitHub Actions CI/CD
✅ Execution Scripts (Week 1-4)

## 🔒 Sicherheit

⚠️ `.env` wird NICHT gepusht (in .gitignore)
⚠️ API-Keys sind sicher
✅ Nur `.env.example` wird gepusht

## 🎯 Nächste Schritte

1. GitHub Secrets setzen (Settings → Secrets)
2. GitHub Pages aktivieren (optional)
3. Branch Protection Rules (optional)
4. Deployment konfigurieren
