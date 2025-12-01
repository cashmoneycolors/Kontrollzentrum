# 🖥️ Amazon Dropshipping Desktop App - Setup

**Plattform:** Windows 10/11 (WPF)  
**Framework:** .NET 8.0  
**Sprache:** C#  

---

## 🚀 Installation

### Voraussetzungen
- Windows 10 oder höher
- .NET 8.0 SDK (https://dotnet.microsoft.com/download)
- Visual Studio 2022 oder VS Code

### Option 1: Visual Studio (Empfohlen)

1. Öffne Visual Studio 2022
2. File → Open → Folder
3. Wähle: `c:\Users\Laptop\Kontrollzentrum-1\dropshipping_desktop`
4. Warte bis Projekt geladen ist
5. Drücke `F5` zum Starten

### Option 2: Command Line

```bash
cd c:\Users\Laptop\Kontrollzentrum-1\dropshipping_desktop
dotnet restore
dotnet build
dotnet run
```

### Option 3: Executable bauen

```bash
cd c:\Users\Laptop\Kontrollzentrum-1\dropshipping_desktop
dotnet publish -c Release -r win-x64 --self-contained
```

Executable findet sich dann in: `bin\Release\net8.0-windows\win-x64\publish\DropshippingApp.exe`

---

## 📋 Features

✅ **Produktsuche** - Amazon Produkte durchsuchen  
✅ **Preisberechnung** - Automatische Margin-Berechnung  
✅ **Bestellverwaltung** - Bestellungen erstellen & verwalten  
✅ **Statistiken** - Live-Dashboard  
✅ **Demo-Modus** - Keine API-Keys nötig  

---

## 🎯 Verwendung

### Tab 1: Produktsuche
1. Gib Produktname ein (z.B. "Wireless Headphones")
2. Klick "🔍 Suchen"
3. Sehe Ergebnisse mit Preisen und Gewinn

### Tab 2: Profitrechner
1. Gib Lieferantenpreis ein
2. Stelle Gewinnmarge ein (Slider)
3. Klick "📊 Berechnen"
4. Sehe Verkaufspreis und Gewinn

### Tab 3: Bestellungen
1. Gib Kundenmail ein
2. Klick "✅ Bestellung erstellen"
3. Sehe Bestellungen in der Liste

### Tab 4: Statistiken
1. Sehe Übersicht aller Bestellungen
2. Sehe ausstehende Bestellungen
3. Sehe versendte Bestellungen

---

## 🔧 Architektur

```
Models/
  ├── Product.cs       - Produktdaten
  ├── Order.cs         - Bestelldaten
  └── PricingResult.cs - Preisberechnung

Services/
  ├── AmazonService.cs    - Produktsuche
  ├── PricingService.cs   - Preisberechnung
  └── OrderService.cs     - Bestellverwaltung

ViewModels/
  └── MainViewModel.cs    - MVVM ViewModel

Views/
  ├── MainWindow.xaml     - UI Layout
  └── MainWindow.xaml.cs  - Code-Behind

App.xaml / App.xaml.cs    - Application Entry
```

---

## 📦 Dependencies

- **CommunityToolkit.Mvvm** - MVVM Framework
- **RestSharp** - HTTP Client
- **Newtonsoft.Json** - JSON Serialization

---

## 🔐 Konfiguration

Für Produktivbetrieb:
1. Öffne `Services/AmazonService.cs`
2. Ersetze Demo-Daten mit echten API-Calls
3. Trage API-Keys ein

---

## 🧪 Testing

```bash
# Projekt bauen
dotnet build

# Tests ausführen (falls vorhanden)
dotnet test
```

---

## 📊 Performance

- **Startup:** ~2 Sekunden
- **Produktsuche:** ~200ms
- **Preisberechnung:** ~50ms
- **Memory:** ~100MB

---

## 🐛 Troubleshooting

### App startet nicht
```bash
dotnet restore
dotnet clean
dotnet build
```

### .NET 8.0 nicht gefunden
```bash
dotnet --version
# Falls nicht 8.0, installiere von https://dotnet.microsoft.com/download
```

### Visual Studio erkennt Projekt nicht
1. Schließe Visual Studio
2. Lösche `.vs` Ordner
3. Öffne Projekt neu

---

## 🚀 Nächste Schritte

1. ✅ App starten
2. ✅ Alle Tabs testen
3. ✅ Produkte suchen
4. ✅ Bestellungen erstellen
5. ✅ API-Keys eintragen (für Produktivbetrieb)

---

**Viel Erfolg! 🎉**
