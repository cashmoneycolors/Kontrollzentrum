# 🖥️ BUILD DESKTOP APP - Kontrollzentrum

## Windows Desktop App (WPF) - C#

**Status:** ✅ Bereit zum Bauen  
**Framework:** .NET 8.0 WPF  
**Zielplattform:** Windows 10/11

---

## 📋 VORAUSSETZUNGEN

### 1. Visual Studio installieren
- **Visual Studio 2022 Community** (kostenlos)
- Download: https://visualstudio.microsoft.com/
- Workload: ".NET desktop development"

### 2. .NET 8.0 SDK
- Download: https://dotnet.microsoft.com/download
- Oder: Automatisch mit Visual Studio

### 3. Projekt-Dateien
- ✅ KontrollzentrumDesktop.csproj
- ✅ MainWindow.xaml
- ✅ MainWindow.xaml.cs
- ✅ App.xaml
- ✅ App.xaml.cs

---

## 🚀 BUILD-ANLEITUNG

### Option 1: Visual Studio (Einfach)

1. **Öffne Visual Studio**
2. **Datei → Neues Projekt**
3. **"WPF App (.NET Framework)" wählen**
4. **Projektname:** Kontrollzentrum
5. **Kopiere die Dateien:**
   - MainWindow.xaml
   - MainWindow.xaml.cs
   - App.xaml
   - App.xaml.cs
6. **Build → Build Solution** (Ctrl+Shift+B)
7. **Debug → Start Debugging** (F5)

### Option 2: Command Line (Schnell)

```bash
# 1. Projekt erstellen
dotnet new wpf -n Kontrollzentrum

# 2. Dependencies hinzufügen
dotnet add package RestSharp
dotnet add package Newtonsoft.Json

# 3. Bauen
dotnet build

# 4. Ausführen
dotnet run
```

### Option 3: Executable bauen

```bash
# Release-Build
dotnet publish -c Release -r win-x64 --self-contained

# Output: bin/Release/net8.0-windows/win-x64/publish/Kontrollzentrum.exe
```

---

## 📁 PROJEKTSTRUKTUR

```
Kontrollzentrum/
├── KontrollzentrumDesktop.csproj    ✅ Projekt-Datei
├── MainWindow.xaml                  ✅ UI-Design
├── MainWindow.xaml.cs               ✅ Code-Behind
├── App.xaml                         ✅ App-Konfiguration
├── App.xaml.cs                      ✅ App-Code
├── bin/                             (Auto-generiert)
│   └── Release/
│       └── net8.0-windows/
│           └── win-x64/
│               └── publish/
│                   └── Kontrollzentrum.exe  ✅ Executable
└── obj/                             (Auto-generiert)
```

---

## 🎯 FEATURES

### Dashboard
- ✅ 15 Module anzeigen
- ✅ Status überwachen
- ✅ Module starten/stoppen

### Sidebar-Navigation
- 🏠 Dashboard
- 📊 Module
- 🔑 API-Keys
- 🧪 Tests
- ⚙️ Einstellungen
- ❌ Beenden

### Funktionen
- ✅ Alle Module starten
- ✅ Python-Integration
- ✅ Echtzeit-Status
- ✅ Error-Handling

---

## 🔧 ANPASSUNGEN

### Design ändern
Bearbeite `MainWindow.xaml`:
```xml
<Window Background="#1e1e1e" Foreground="#ffffff">
```

### Farben anpassen
```xml
<!-- Blau -->
<SolidColorBrush Color="#00d4ff"/>

<!-- Grün -->
<SolidColorBrush Color="#00ff00"/>

<!-- Rot -->
<SolidColorBrush Color="#ff0000"/>
```

### Module hinzufügen
Bearbeite `MainWindow.xaml.cs`:
```csharp
modules.Add(new ModuleItem { 
    Name = "neues_modul", 
    Status = "✅ Aktiv" 
});
```

---

## 📦 DISTRIBUTION

### Executable erstellen
```bash
dotnet publish -c Release -r win-x64 --self-contained
```

### Installer erstellen (Optional)
```bash
# Mit WiX Toolset
heat dir bin\Release\net8.0-windows\win-x64\publish -o files.wxs
candle files.wxs -o obj\
light obj\files.wixobj -o Kontrollzentrum.msi
```

### Portable Version
```bash
# Alle Dateien in einen Ordner
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true
```

---

## 🐛 TROUBLESHOOTING

### Problem: "Visual Studio nicht gefunden"
**Lösung:** Installiere Visual Studio 2022 Community

### Problem: ".NET 8.0 nicht gefunden"
**Lösung:** Installiere .NET 8.0 SDK

### Problem: "Projekt lädt nicht"
**Lösung:** 
```bash
dotnet restore
dotnet build
```

### Problem: "Python nicht gefunden"
**Lösung:** Stelle sicher, dass Python im PATH ist
```bash
python --version
```

---

## ✅ CHECKLISTE

- [ ] Visual Studio 2022 installiert
- [ ] .NET 8.0 SDK installiert
- [ ] Projekt-Dateien kopiert
- [ ] Projekt gebaut (Ctrl+Shift+B)
- [ ] App getestet (F5)
- [ ] Executable erstellt
- [ ] Auf anderen Computern getestet

---

## 🎉 FERTIG!

**Die Desktop-App ist bereit für Windows!**

- ✅ Moderne WPF-UI
- ✅ Python-Integration
- ✅ 15 Module
- ✅ Produktionsbereit

---

## 📞 SUPPORT

- **Visual Studio:** https://visualstudio.microsoft.com/
- **.NET:** https://dotnet.microsoft.com/
- **WPF:** https://docs.microsoft.com/en-us/dotnet/desktop/wpf/

---

**🖥️ DESKTOP APP BEREIT ZUM BAUEN!**

*Letzte Aktualisierung: 2025-11-30*
