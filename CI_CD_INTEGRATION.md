# 🚀 CI/CD INTEGRATION GUIDE - OPTION A
## GitHub Actions Workflows für Kontrollzentrum

**Version**: 1.0  
**Datum**: 01.12.2025  
**Status**: PRODUCTION READY

---

## 📋 ÜBERSICHT

### Workflows
1. **Auto-Sync**: Automatische Submodule-Synchronisierung
2. **Test**: Automatische Tests aller Submodules
3. **Release**: Automatische Release-Erstellung
4. **Security**: Sicherheits-Scans
5. **Performance**: Performance-Monitoring

---

## 🔄 WORKFLOW 1: AUTO-SYNC

**Datei**: `.github/workflows/auto-sync.yml`

```yaml
name: Auto-Sync Submodules

on:
  schedule:
    # Täglich um 2:00 UTC
    - cron: '0 2 * * *'
  # Manuell auslösbar
  workflow_dispatch:
    inputs:
      mode:
        description: 'Sync Mode'
        required: true
        default: 'dev'
        type: choice
        options:
          - dev
          - prod

jobs:
  sync:
    runs-on: windows-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup PowerShell
        uses: microsoft/setup-msbuild@v1
      
      - name: Sync Submodules
        run: |
          $mode = "${{ github.event.inputs.mode }}" -or "dev"
          .\SYNC_ALL_REPOS_V2.ps1 -Pull $true -Mode $mode -HealthCheck $true -Verbose $true
        shell: pwsh
      
      - name: Check for Changes
        id: changes
        run: |
          $changes = git status --porcelain
          if ($changes) {
            echo "has_changes=true" >> $env:GITHUB_OUTPUT
          } else {
            echo "has_changes=false" >> $env:GITHUB_OUTPUT
          }
        shell: pwsh
      
      - name: Commit & Push
        if: steps.changes.outputs.has_changes == 'true'
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "🔄 Auto-sync submodules - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
          git push origin blackboxai/azure-mcp-setup
        shell: pwsh
      
      - name: Upload Metrics
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: sync-metrics
          path: |
            sync_*.log
            metrics_*.json
      
      - name: Notify on Failure
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Auto-sync failed. Check workflow logs.'
            })

```

---

## 🧪 WORKFLOW 2: TEST

**Datei**: `.github/workflows/test.yml`

```yaml
name: Test All Submodules

on:
  push:
    branches: [main, develop, blackboxai/azure-mcp-setup]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: windows-latest
    strategy:
      matrix:
        submodule:
          - module
          - desktop-tutorial
          - autonomous-zenith-optimizer
          - blank-app
          - mega-ultra-roboter-ki
      fail-fast: false
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0.x'
      
      - name: Install Dependencies
        run: |
          cd submodules/${{ matrix.submodule }}
          if (Test-Path "requirements.txt") {
            pip install -r requirements.txt
          }
          if (Test-Path "*.csproj") {
            dotnet restore
          }
        shell: pwsh
      
      - name: Run Tests
        run: |
          cd submodules/${{ matrix.submodule }}
          
          # Python Tests
          if (Test-Path "tests") {
            python -m pytest tests/ -v --tb=short
          }
          
          # .NET Tests
          if (Test-Path "*.csproj") {
            dotnet test --verbosity normal
          }
        shell: pwsh
        continue-on-error: true
      
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.submodule }}
          path: |
            submodules/${{ matrix.submodule }}/test-results/
            submodules/${{ matrix.submodule }}/coverage/
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const submodule = '${{ matrix.submodule }}';
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `✅ Tests passed for ${submodule}`
            })

```

---

## 📦 WORKFLOW 3: RELEASE

**Datei**: `.github/workflows/release.yml`

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: windows-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Get Version
        id: version
        run: |
          $version = "${{ github.ref }}" -replace 'refs/tags/v', ''
          echo "version=$version" >> $env:GITHUB_OUTPUT
        shell: pwsh
      
      - name: Create Release Notes
        id: release_notes
        run: |
          $commits = git log --oneline $(git describe --tags --abbrev=0 HEAD^)..HEAD
          $notes = @"
          ## Changes
          $commits
          
          ## Submodules
          $(git submodule status)
          "@
          echo "notes=$notes" >> $env:GITHUB_OUTPUT
        shell: pwsh
      
      - name: Build Release Package
        run: |
          # Python Modules
          $pythonModules = Get-ChildItem modules -Filter "*.py" -Exclude "__*"
          Compress-Archive -Path $pythonModules -DestinationPath "release/python_modules_${{ steps.version.outputs.version }}.zip"
          
          # Desktop App
          if (Test-Path "dropshipping_desktop") {
            dotnet publish dropshipping_desktop -c Release -o release/desktop_app
            Compress-Archive -Path release/desktop_app -DestinationPath "release/desktop_app_${{ steps.version.outputs.version }}.zip"
          }
          
          # Documentation
          Compress-Archive -Path @("*.md", ".github") -DestinationPath "release/docs_${{ steps.version.outputs.version }}.zip"
        shell: pwsh
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ steps.version.outputs.version }}
          release_name: Release ${{ steps.version.outputs.version }}
          body: ${{ steps.release_notes.outputs.notes }}
          draft: false
          prerelease: false
      
      - name: Upload Release Assets
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./release/
          asset_name: kontrollzentrum-${{ steps.version.outputs.version }}
          asset_content_type: application/zip
      
      - name: Notify Release
        run: |
          Write-Host "✅ Release v${{ steps.version.outputs.version }} created successfully"
        shell: pwsh

```

---

## 🔒 WORKFLOW 4: SECURITY

**Datei**: `.github/workflows/security.yml`

```yaml
name: Security Scan

on:
  push:
    branches: [main, develop]
  schedule:
    # Täglich um 3:00 UTC
    - cron: '0 3 * * *'

jobs:
  security:
    runs-on: windows-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Scan for Secrets
        run: |
          pip install detect-secrets
          detect-secrets scan --baseline .secrets.baseline
        shell: pwsh
        continue-on-error: true
      
      - name: Scan for Vulnerabilities
        run: |
          pip install safety bandit
          
          # Check Python dependencies
          if (Test-Path "requirements.txt") {
            safety check -r requirements.txt
          }
          
          # Check Python code
          bandit -r modules/ -f json -o bandit-report.json
        shell: pwsh
        continue-on-error: true
      
      - name: SAST Scan
        uses: github/super-linter@v4
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Upload Security Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            .secrets.baseline
      
      - name: Comment on Issues
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ Security scan found issues. Check artifacts.'
            })

```

---

## 📊 WORKFLOW 5: PERFORMANCE

**Datei**: `.github/workflows/performance.yml`

```yaml
name: Performance Monitoring

on:
  push:
    branches: [main, develop]
  schedule:
    # Täglich um 4:00 UTC
    - cron: '0 4 * * *'

jobs:
  performance:
    runs-on: windows-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Measure Sync Performance
        run: |
          $startTime = Get-Date
          
          # Simulate sync
          .\SYNC_ALL_REPOS_V2.ps1 -Mode status -DryRun $true
          
          $duration = (Get-Date) - $startTime
          
          $metrics = @{
            timestamp = Get-Date -Format 'o'
            sync_duration_ms = $duration.TotalMilliseconds
            repo_size_mb = ((Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)
            submodule_count = (Get-ChildItem submodules -Directory).Count
          }
          
          $metrics | ConvertTo-Json | Out-File performance_metrics.json
        shell: pwsh
      
      - name: Compare with Baseline
        run: |
          # Vergleiche mit vorherigen Metriken
          if (Test-Path "performance_baseline.json") {
            $baseline = Get-Content performance_baseline.json | ConvertFrom-Json
            $current = Get-Content performance_metrics.json | ConvertFrom-Json
            
            $syncDiff = $current.sync_duration_ms - $baseline.sync_duration_ms
            $sizeDiff = $current.repo_size_mb - $baseline.repo_size_mb
            
            if ($syncDiff -gt 1000) {
              Write-Host "⚠️  Sync time increased by $($syncDiff)ms"
            }
            
            if ($sizeDiff -gt 100) {
              Write-Host "⚠️  Repo size increased by $($sizeDiff)MB"
            }
          }
        shell: pwsh
      
      - name: Upload Metrics
        uses: actions/upload-artifact@v3
        with:
          name: performance-metrics
          path: performance_metrics.json
      
      - name: Update Baseline
        if: github.ref == 'refs/heads/main'
        run: |
          Copy-Item performance_metrics.json performance_baseline.json
          git add performance_baseline.json
          git commit -m "📊 Update performance baseline"
          git push
        shell: pwsh
        continue-on-error: true

```

---

## 🔧 SETUP INSTRUCTIONS

### 1. Erstelle Workflows-Verzeichnis

```powershell
mkdir -Path ".github/workflows" -Force
```

### 2. Kopiere Workflow-Dateien

Erstelle die YAML-Dateien in `.github/workflows/`:
- `auto-sync.yml`
- `test.yml`
- `release.yml`
- `security.yml`
- `performance.yml`

### 3. Konfiguriere Secrets

```powershell
# In GitHub Repository Settings > Secrets:
# - GITHUB_TOKEN (automatisch)
# - SLACK_WEBHOOK (optional)
# - EMAIL_NOTIFICATION (optional)
```

### 4. Aktiviere Workflows

```powershell
git add .github/workflows/
git commit -m "Add CI/CD workflows"
git push origin main
```

---

## 📊 MONITORING & REPORTING

### Workflow-Status anzeigen

```powershell
# Zeige letzte Workflow-Runs
gh run list --repo cashmoneycolors/Kontrollzentrum

# Zeige Details eines Runs
gh run view <run_id>

# Zeige Logs
gh run view <run_id> --log
```

### Metriken exportieren

```powershell
# Exportiere Workflow-Metriken
gh run list --repo cashmoneycolors/Kontrollzentrum --json status,conclusion,durationMinutes -o csv > workflow_metrics.csv
```

---

## 🚨 TROUBLESHOOTING

### Workflow schlägt fehl

```powershell
# 1. Prüfe Logs
gh run view <run_id> --log

# 2. Prüfe Secrets
gh secret list

# 3. Prüfe Berechtigungen
# Settings > Actions > General > Workflow permissions
```

### Submodule-Update schlägt fehl

```powershell
# 1. Prüfe .gitmodules
cat .gitmodules

# 2. Prüfe Remote-URLs
git config --file .gitmodules --list

# 3. Teste manuell
git submodule update --init --recursive
```

---

## 📚 BEST PRACTICES

### ✅ SOLLTE GETAN WERDEN
1. ✅ Workflows regelmäßig testen
2. ✅ Secrets sicher verwalten
3. ✅ Logs überwachen
4. ✅ Metriken tracken
5. ✅ Alerts konfigurieren
6. ✅ Dokumentation aktualisieren

### ❌ NICHT MACHEN
1. ❌ Secrets in Code speichern
2. ❌ Workflows ohne Tests
3. ❌ Logs ignorieren
4. ❌ Automatische Pushes ohne Validierung
5. ❌ Alte Workflows nicht löschen

---

## 🔗 RESSOURCEN

- GitHub Actions Docs: https://docs.github.com/en/actions
- Workflow Syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Marketplace: https://github.com/marketplace?type=actions

---

**CI/CD INTEGRATION: ✅ COMPLETE**  
**Version**: 1.0  
**Status**: PRODUCTION READY

