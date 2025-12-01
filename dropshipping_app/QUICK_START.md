# ⚡ Quick Start - 5 Minuten

## Windows 10 HP Laptop Setup

### Option 1: Automatisch (Empfohlen)

**Doppelklick auf diese Datei:**
```
start_app.bat
```

Das startet automatisch:
- ✅ API Server (Port 8000)
- ✅ Dashboard (Port 8501)

Dann öffne im Browser:
- **Dashboard:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

---

### Option 2: Manuell

**Terminal 1 - API Server:**
```bash
cd c:\Users\Laptop\Kontrollzentrum-1\dropshipping_app
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Dashboard:**
```bash
cd c:\Users\Laptop\Kontrollzentrum-1\dropshipping_app
streamlit run dashboard.py
```

---

### Option 3: Tests ausführen

**Doppelklick auf:**
```
run_tests.bat
```

Oder manuell:
```bash
python test_app.py
```

---

## 🎯 Was funktioniert sofort

✅ **Produktsuche** - Suche nach beliebigen Produkten  
✅ **Preisberechnung** - Automatische Margin-Berechnung  
✅ **Lieferantenverwaltung** - Beste Lieferanten finden  
✅ **Bestellverwaltung** - Bestellungen erstellen & verfolgen  
✅ **Dashboard** - Echtzeit-Statistiken  
✅ **REST API** - Alle Endpoints verfügbar  

---

## 📊 Demo-Daten

Die App läuft im **Demo-Modus** - keine echten API-Keys nötig!

**Beispiel-Produkte:**
- Wireless Headphones
- Smartphone Case
- USB Cable
- Power Bank

**Beispiel-Lieferanten:**
- Alibaba (14 Tage Lieferzeit)
- DHGate (10 Tage Lieferzeit)
- 1688 (7 Tage Lieferzeit)

---

## 🔧 Troubleshooting

### Port 8000 bereits in Verwendung?
```bash
# Finde Prozess
netstat -ano | findstr :8000

# Oder nutze anderen Port
python main.py --port 8001
```

### Python nicht gefunden?
```bash
# Installiere Python 3.10+
# https://www.python.org/downloads/

# Oder nutze Windows Store
# https://apps.microsoft.com/store/detail/python/9NRWMJP3717K
```

### Dependencies fehlen?
```bash
pip install -r requirements.txt --upgrade
```

---

## 📈 Nächste Schritte

1. ✅ App starten
2. ✅ Dashboard öffnen
3. ✅ Produkt suchen
4. ✅ Bestellung erstellen
5. ✅ Statistiken anschauen
6. ✅ Profitrechner testen

---

## 🚀 Für Produktivbetrieb

1. Öffne `.env`
2. Trage echte API-Keys ein:
   - `AMAZON_API_KEY`
   - `SUPPLIER_API_KEY`
   - `STRIPE_API_KEY`
3. Starte App neu

---

**Viel Spaß! 🎉**
