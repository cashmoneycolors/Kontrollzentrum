# 🖥️ INSTALLATION GUIDE - Desktop App

**Kontrollzentrum - Windows Desktop Application**

---

## ⚡ SCHNELLINSTALLATION (5 Minuten)

### Schritt 1: .NET 8.0 SDK installieren
```
1. Öffne: https://dotnet.microsoft.com/download
2. Lade .NET 8.0 SDK herunter
3. Installiere (Next → Next → Finish)
4. Starte Terminal neu
```

### Schritt 2: Setup-Skript ausführen
```powershell
# PowerShell als Administrator öffnen
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_desktop_app.ps1
```

### Schritt 3: App starten
```bash
cd KontrollzentrumApp
dotnet run
```

---

## 📋 DETAILLIERTE INSTALLATION

### Option A: Visual Studio 2022 (Empfohlen)

**1. Visual Studio 2022 installieren**
- Download: https://visualstudio.microsoft.com/
- Wähle: "Desktop development with C++"
- Installiere

**2. Projekt öffnen**
- Visual Studio starten
- File → Open → Folder
- Wähle: `KontrollzentrumApp`

**3. App starten**
- Drücke: `F5`
- App öffnet sich

**4. Executable bauen**
- Build → Build Solution
- Output: `bin/Release/net8.0-windows/win-x64/publish/Kontrollzentrum.exe`

---

### Option B: Command Line (Schnell)

**1. Terminal öffnen**
```bash
cd KontrollzentrumApp
```

**2. Abhängigkeiten installieren**
```bash
dotnet restore
```

**3. Projekt bauen**
```bash
dotnet build
```

**4. App starten**
```bash
dotnet run
```

**5. Executable bauen**
```bash
dotnet publish -c Release -r win-x64 --self-contained
```

---

### Option C: Automatisches Setup (Empfohlen)

**1. PowerShell als Administrator öffnen**

**2. Ausführungsrichtlinie ändern**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. Setup-Skript ausführen**
```powershell
.\setup_desktop_app.ps1
```

**4. App starten**
```bash
cd KontrollzentrumApp
dotnet run
```

---

## 🔧 VORAUSSETZUNGEN

### Erforderlich
- ✅ Windows 10/11
- ✅ .NET 8.0 SDK
- ✅ Python 3.8+ (für Module)

### Optional
- ⭕ Visual Studio 2022 (für Entwicklung)
- ⭕ Git (für Versionskontrolle)

---

## 📦 DATEIEN

### C# Dateien (5)
```
KontrollzentrumDesktop.csproj    Projekt-Konfiguration
MainWindow.xaml                  UI-Design
MainWindow.xaml.cs               Code-Behind
App.xaml                         App-Konfiguration
App.xaml.cs                      App-Code
```

### Setup-Dateien
```
setup_desktop_app.ps1            Automatisches Setup
INSTALL_DESKTOP_APP.md           Diese Anleitung
BUILD_DESKTOP_APP.md             Detaillierte Build-Anleitung
DESKTOP_APP_QUICK_START.txt      Quick Start
DESKTOP_APP_SUMMARY.md           Zusammenfassung
```

---

## 🚀 STARTEN

### Nach Installation
```bash
cd KontrollzentrumApp
dotnet run
```

### App-Fenster
- Sidebar mit Navigation
- Dashboard mit Modulen
- Buttons zum Starten/Stoppen
- Status-Anzeige

---

## 🐛 TROUBLESHOOTING

### Problem: ".NET 8.0 nicht gefunden"
```powershell
# Prüfe Installation
dotnet --version

# Installiere .NET 8.0
# Download: https://dotnet.microsoft.com/download
```

### Problem: "Projekt lädt nicht"
```bash
dotnet restore
dotnet build
```

### Problem: "Python nicht gefunden"
```bash
# Prüfe Python-Installation
python --version

# Stelle sicher, dass Python im PATH ist
```

### Problem: "Fehler beim Bauen"
```bash
# Lösche Cache
rm -r bin obj

# Baue neu
dotnet build
```

---

## 📊 VERZEICHNISSTRUKTUR

```
KontrollzentrumApp/
├── KontrollzentrumDesktop.csproj
├── MainWindow.xaml
├── MainWindow.xaml.cs
├── App.xaml
├── App.xaml.cs
├── bin/
│   └── Release/
│       └── net8.0-windows/
│           └── win-x64/
│               └── publish/
│                   └── Kontrollzentrum.exe
└── obj/
```

---

## ✅ CHECKLISTE

- [ ] .NET 8.0 SDK installiert
- [ ] Setup-Skript ausgeführt
- [ ] Projekt gebaut
- [ ] App getestet (F5)
- [ ] Executable erstellt
- [ ] Auf anderen Computern getestet

---

## 📞 SUPPORT

- **.NET:** https://dotnet.microsoft.com/
- **Visual Studio:** https://visualstudio.microsoft.com/
- **WPF:** https://docs.microsoft.com/en-us/dotnet/desktop/wpf/

---

## 🎉 FERTIG!

**Die Desktop-App ist installiert und bereit!**

```bash
cd KontrollzentrumApp
dotnet run
```

---

**🖥️ DESKTOP APP INSTALLIERT!**

*Letzte Aktualisierung: 2025-11-30*
