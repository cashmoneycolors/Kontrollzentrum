# 🔧 TROUBLESHOOTING GUIDE - OPTION A ORCHESTRATION
## Kontrollzentrum Submodule Management

**Version**: 2.0  
**Datum**: 01.12.2025  
**Status**: PRODUCTION READY

---

## 📋 INHALTSVERZEICHNIS

1. [Häufige Probleme](#häufige-probleme)
2. [Diagnose-Tools](#diagnose-tools)
3. [Lösungsstrategien](#lösungsstrategien)
4. [Notfall-Verfahren](#notfall-verfahren)
5. [Performance-Optimierung](#performance-optimierung)
6. [Sicherheit & Compliance](#sicherheit--compliance)

---

## 🚨 HÄUFIGE PROBLEME

### Problem 1: Sync schlägt fehl

**Symptome:**
```
❌ Sync failed for module
Error: merge conflict
```

**Diagnose:**
```powershell
# 1. Prüfe Git-Status
cd submodules/module
git status

# 2. Prüfe Konflikte
git diff --name-only --diff-filter=U

# 3. Prüfe Remote
git remote -v
git fetch origin

# 4. Prüfe Logs
git log --oneline -10
```

**Lösungen:**

**Option A: Automatische Auflösung**
```powershell
# Nutze das erweiterte Sync-Script
.\SYNC_ALL_REPOS_V2.ps1 -Pull -Mode dev -HandleConflicts $true
```

**Option B: Manuelle Auflösung**
```powershell
cd submodules/module

# Zeige Konflikte
git diff

# Bearbeite Dateien manuell
# Dann:
git add .
git commit -m "Resolve merge conflicts"
git push origin main

# Zurück zu Parent
cd ../..
git add submodules/module
git commit -m "Update module after conflict resolution"
```

**Option C: Rollback**
```powershell
# Rollback zu letztem guten Zustand
.\SYNC_ALL_REPOS_V2.ps1 -Rollback -CommitHash "abc123def456"
```

---

### Problem 2: Detached HEAD

**Symptome:**
```
⚠️  HEAD detached at abc123
```

**Diagnose:**
```powershell
cd submodules/module
git status
git branch -a
```

**Lösung:**
```powershell
cd submodules/module

# Wechsel zu main branch
git checkout main

# Oder zu develop
git checkout develop

# Aktualisiere
git pull origin main

# Zurück zu Parent
cd ../..
```

---

### Problem 3: Dirty Submodule

**Symptome:**
```
⚠️  Uncommitted changes: 5 files
```

**Diagnose:**
```powershell
cd submodules/module
git status --porcelain
git diff
```

**Lösungen:**

**Option A: Stash & Pull**
```powershell
cd submodules/module

# Speichere Änderungen
git stash

# Aktualisiere
git pull origin main

# Hole Änderungen zurück
git stash pop

# Löse Konflikte (falls nötig)
git add .
git commit -m "Merge stashed changes"
```

**Option B: Verwerfe Änderungen**
```powershell
cd submodules/module

# Verwerfe alle lokalen Änderungen
git reset --hard HEAD

# Aktualisiere
git pull origin main
```

**Option C: Committe Änderungen**
```powershell
cd submodules/module

# Committe Änderungen
git add .
git commit -m "Local changes"

# Push
git push origin main

# Zurück zu Parent
cd ../..
git add submodules/module
git commit -m "Update module"
```

---

### Problem 4: Submodule fehlt

**Symptome:**
```
❓ submodules/module: missing
```

**Diagnose:**
```powershell
# Prüfe .gitmodules
cat .gitmodules

# Prüfe Submodule-Status
git submodule status

# Prüfe Verzeichnis
ls submodules/
```

**Lösung:**
```powershell
# Re-initialisiere Submodules
git submodule init
git submodule update --remote --recursive

# Oder: Entferne und re-klone
git submodule deinit -f submodules/module
git submodule update --init --recursive submodules/module
```

---

### Problem 5: Netzwerkfehler

**Symptome:**
```
❌ fatal: unable to access 'https://github.com/...'
```

**Diagnose:**
```powershell
# Prüfe Netzwerk
Test-Connection github.com

# Prüfe Git-Konfiguration
git config --list

# Prüfe SSH-Keys
ssh -T git@github.com
```

**Lösungen:**

**Option A: HTTPS statt SSH**
```powershell
# Ändere Remote-URL
git remote set-url origin https://github.com/cashmoneycolors/Kontrollzentrum.git

# Für Submodules
git config --file .gitmodules --name-only --get-regexp url | while read url; do
    git config --file .gitmodules --replace-all $url https://...
done
```

**Option B: SSH-Keys konfigurieren**
```powershell
# Generiere SSH-Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Füge zu GitHub hinzu
# https://github.com/settings/keys

# Teste Verbindung
ssh -T git@github.com
```

**Option C: Proxy-Konfiguration**
```powershell
# Wenn hinter Proxy
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080
```

---

### Problem 6: Speicherplatz voll

**Symptome:**
```
❌ fatal: unable to create temporary file
```

**Diagnose:**
```powershell
# Prüfe Disk-Space
Get-Volume

# Prüfe Repo-Größe
(Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
```

**Lösungen:**

**Option A: Cleanup**
```powershell
# Garbage Collection
git gc --aggressive

# Prüne Refs
git prune

# Bereinige Submodules
git submodule foreach git gc --aggressive
```

**Option B: Große Dateien entfernen**
```powershell
# Finde große Dateien
git rev-list --all --objects | sort -k2 | tail -20

# Entferne aus History (BFG Repo-Cleaner)
bfg --delete-files large_file.bin
```

**Option C: Shallow Clone**
```powershell
# Klone nur letzte Commits
git clone --depth 1 https://github.com/cashmoneycolors/Kontrollzentrum.git
```

---

## 🔍 DIAGNOSE-TOOLS

### Automatische Diagnose
```powershell
# Führe vollständige Diagnose durch
function Diagnose-Kontrollzentrum {
    Write-Host "🔍 KONTROLLZENTRUM DIAGNOSE" -ForegroundColor Cyan
    
    # 1. Git-Status
    Write-Host "`n1️⃣  GIT STATUS" -ForegroundColor Magenta
    git status
    
    # 2. Submodule-Status
    Write-Host "`n2️⃣  SUBMODULE STATUS" -ForegroundColor Magenta
    git submodule status --recursive
    
    # 3. Remote-Status
    Write-Host "`n3️⃣  REMOTE STATUS" -ForegroundColor Magenta
    git remote -v
    
    # 4. Netzwerk-Test
    Write-Host "`n4️⃣  NETZWERK TEST" -ForegroundColor Magenta
    Test-Connection github.com -Count 1
    
    # 5. Disk-Space
    Write-Host "`n5️⃣  DISK SPACE" -ForegroundColor Magenta
    Get-Volume | Format-Table
    
    # 6. Repo-Größe
    Write-Host "`n6️⃣  REPO GRÖSSSE" -ForegroundColor Magenta
    (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
    
    # 7. Submodule-Health
    Write-Host "`n7️⃣  SUBMODULE HEALTH" -ForegroundColor Magenta
    Get-ChildItem submodules -Directory | ForEach-Object {
        Push-Location $_.FullName
        $status = git status --porcelain
        $conflicts = git diff --name-only --diff-filter=U
        Write-Host "  $($_.Name): Dirty=$($status.Count) Conflicts=$($conflicts.Count)"
        Pop-Location
    }
}

Diagnose-Kontrollzentrum
```

### Health-Check Script
```powershell
# Detaillierter Health-Check
function Test-SubmoduleHealth {
    param([string]$Submodule)
    
    $health = @{
        Name = Split-Path $Submodule -Leaf
        Status = 'unknown'
        Issues = @()
    }
    
    Push-Location $Submodule
    
    # Prüfe Git-Repo
    if (-not (git rev-parse --git-dir 2>$null)) {
        $health.Status = 'invalid'
        $health.Issues += "Not a valid Git repository"
        Pop-Location
        return $health
    }
    
    # Prüfe Dirty-Status
    $dirty = git status --porcelain
    if ($dirty.Count -gt 0) {
        $health.Issues += "Uncommitted changes: $($dirty.Count) files"
    }
    
    # Prüfe Konflikte
    $conflicts = git diff --name-only --diff-filter=U
    if ($conflicts.Count -gt 0) {
        $health.Issues += "Merge conflicts: $($conflicts.Count) files"
    }
    
    # Prüfe Branch
    $branch = git rev-parse --abbrev-ref HEAD
    if ($branch -eq 'HEAD') {
        $health.Issues += "Detached HEAD state"
    }
    
    # Prüfe Remote
    $remote = git remote -v
    if (-not $remote) {
        $health.Issues += "No remote configured"
    }
    
    # Status bestimmen
    if ($health.Issues.Count -eq 0) {
        $health.Status = 'healthy'
    } elseif ($health.Issues.Count -le 2) {
        $health.Status = 'warning'
    } else {
        $health.Status = 'critical'
    }
    
    Pop-Location
    return $health
}

# Teste alle Submodules
Get-ChildItem submodules -Directory | ForEach-Object {
    $health = Test-SubmoduleHealth $_.FullName
    Write-Host "$($health.Name): $($health.Status)"
    $health.Issues | ForEach-Object { Write-Host "  - $_" }
}
```

---

## 🛠️ LÖSUNGSSTRATEGIEN

### Strategie 1: Schrittweise Wiederherstellung

```powershell
# 1. Backup erstellen
Copy-Item -Path "submodules" -Destination "submodules_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse

# 2. Status prüfen
git status
git submodule status

# 3. Probleme identifizieren
Get-ChildItem submodules -Directory | ForEach-Object {
    Push-Location $_.FullName
    $status = git status --porcelain
    if ($status.Count -gt 0) {
        Write-Host "Problem in $($_.Name): $($status.Count) dirty files"
    }
    Pop-Location
}

# 4. Probleme beheben
# (siehe spezifische Lösungen oben)

# 5. Verifizieren
.\SYNC_ALL_REPOS_V2.ps1 -HealthCheck $true
```

### Strategie 2: Vollständiger Reset

```powershell
# ⚠️  WARNUNG: Dies verwirft alle lokalen Änderungen!

# 1. Backup
Copy-Item -Path "." -Destination "kontrollzentrum_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse

# 2. Reset Parent
git reset --hard HEAD
git clean -fd

# 3. Reset Submodules
git submodule foreach git reset --hard HEAD
git submodule foreach git clean -fd

# 4. Re-initialisiere
git submodule deinit -f --all
git submodule init
git submodule update --remote --recursive

# 5. Verifiziere
git status
git submodule status
```

### Strategie 3: Selektive Wiederherstellung

```powershell
# Stelle nur ein Submodule wieder her

$submodule = "submodules/module"

# 1. Backup
Copy-Item -Path $submodule -Destination "$submodule.backup" -Recurse

# 2. Entferne
git submodule deinit -f $submodule
git rm -f $submodule

# 3. Re-klone
git submodule add https://github.com/cashmoneycolors/module.git $submodule
git submodule update --init --recursive $submodule

# 4. Committe
git add .gitmodules $submodule
git commit -m "Restore $submodule"
```

---

## 🚨 NOTFALL-VERFAHREN

### Notfall 1: Kritischer Fehler - Sofortiger Rollback

```powershell
# 1. Identifiziere letzten guten Commit
git log --oneline -20

# 2. Rollback
git reset --hard <commit_hash>

# 3. Erzwinge Push (nur wenn nötig!)
git push origin main --force

# 4. Benachrichtige Team
Write-Host "⚠️  ROLLBACK DURCHGEFÜHRT!" -ForegroundColor Red
Write-Host "Commit: <commit_hash>" -ForegroundColor Yellow
```

### Notfall 2: Korruption erkannt

```powershell
# 1. Erstelle sofort Backup
Copy-Item -Path "." -Destination "emergency_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse

# 2. Versuche Reparatur
git fsck --full

# 3. Wenn Reparatur fehlschlägt: Neu-klone
git clone --recurse-submodules https://github.com/cashmoneycolors/Kontrollzentrum.git kontrollzentrum_new

# 4. Migriere lokale Änderungen
# (manuell von Backup)
```

### Notfall 3: Netzwerk-Ausfall

```powershell
# 1. Arbeite offline
# - Committe lokal
# - Nutze lokale Branches

# 2. Wenn Netzwerk zurück:
git fetch origin
git merge origin/main

# 3. Push
git push origin main
```

---

## ⚡ PERFORMANCE-OPTIMIERUNG

### Schnellere Syncs

```powershell
# 1. Shallow Clone (nur letzte Commits)
git clone --depth 1 --recurse-submodules https://github.com/cashmoneycolors/Kontrollzentrum.git

# 2. Parallele Operationen
git config --global submodule.fetchJobs 4

# 3. Größere Buffer
git config --global http.postBuffer 524288000

# 4. Caching
git config --global credential.helper store
```

### Speicheroptimierung

```powershell
# 1. Garbage Collection
git gc --aggressive

# 2. Prune
git prune

# 3. Submodule Cleanup
git submodule foreach git gc --aggressive

# 4. Entferne große Dateien
git rev-list --all --objects | sort -k2 | tail -20
```

### Netzwerk-Optimierung

```powershell
# 1. SSH statt HTTPS (schneller)
git remote set-url origin git@github.com:cashmoneycolors/Kontrollzentrum.git

# 2. Compression
git config --global core.compression 9

# 3. Delta-Compression
git config --global pack.deltaCacheSize 2g
```

---

## 🔐 SICHERHEIT & COMPLIANCE

### Secrets-Schutz

```powershell
# 1. Prüfe auf Secrets
git log -p | grep -i "password\|api_key\|secret"

# 2. Entferne Secrets aus History
# Nutze BFG Repo-Cleaner
bfg --replace-text secrets.txt

# 3. Konfiguriere .gitignore
@"
.env
*.key
*.pem
secrets.json
"@ | Out-File .gitignore -Append
```

### Access-Control

```powershell
# 1. Prüfe Berechtigungen
git config --list | grep user

# 2. Konfiguriere GPG-Signing
git config --global user.signingkey <key_id>
git config --global commit.gpgSign true

# 3. Prüfe Commits
git log --show-signature
```

### Audit-Logging

```powershell
# 1. Aktiviere Reflog
git config --global core.logAllRefUpdates true

# 2. Prüfe Logs
git reflog

# 3. Exportiere Audit-Trail
git log --all --oneline > audit_trail.txt
```

---

## 📞 SUPPORT & ESKALATION

### Wann Support kontaktieren?

- ❌ Kritische Fehler, die nicht behoben werden können
- ❌ Datenverlust oder Korruption
- ❌ Sicherheitsverletzungen
- ❌ Netzwerk-Probleme, die nicht lokal lösbar sind

### Support-Kontakt

```
Email: support@example.com
Slack: #kontrollzentrum-support
GitHub Issues: https://github.com/cashmoneycolors/Kontrollzentrum/issues
```

### Informationen für Support

```powershell
# Sammle Diagnose-Informationen
$diagnostics = @{
    Timestamp = Get-Date
    GitVersion = git --version
    PowerShellVersion = $PSVersionTable.PSVersion
    RepoStatus = git status
    SubmoduleStatus = git submodule status
    LastCommits = git log --oneline -10
    Errors = @()
}

$diagnostics | ConvertTo-Json | Out-File "diagnostics_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
```

---

## 📚 WEITERE RESSOURCEN

- Git Docs: https://git-scm.com/doc
- GitHub Help: https://docs.github.com/en
- Submodules Guide: https://git-scm.com/book/en/v2/Git-Tools-Submodules
- BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/

---

**TROUBLESHOOTING GUIDE: ✅ COMPLETE**  
**Version**: 2.0  
**Status**: PRODUCTION READY

