# 🛍️ Amazon Dropshipping App

Vollständige Dropshipping-Lösung für Amazon mit automatischer Preisberechnung, Lieferantenverwaltung und Bestellautomatisierung.

## ✨ Features

- ✅ **Produktsuche** - Amazon API Integration
- ✅ **Intelligente Preisberechnung** - Automatische Margin-Berechnung
- ✅ **Lieferantenverwaltung** - Alibaba, DHGate, 1688 Integration
- ✅ **Bestellverwaltung** - Automatische Fulfillment
- ✅ **Dashboard** - Echtzeit-Statistiken mit Streamlit
- ✅ **REST API** - FastAPI Backend

## 🚀 Quick Start

### 1. Installation

```bash
cd dropshipping_app
pip install -r requirements.txt
```

### 2. Konfiguration

```bash
cp .env.example .env
# Bearbeite .env mit deinen API-Keys
```

### 3. Starten

**Terminal 1 - API Server:**
```bash
python main.py
```

**Terminal 2 - Dashboard:**
```bash
streamlit run dashboard.py
```

## 📊 API Endpoints

| Endpoint | Methode | Beschreibung |
|----------|---------|-------------|
| `/health` | GET | Health Check |
| `/search` | POST | Produkte suchen |
| `/product/{asin}` | GET | Produktdetails |
| `/orders` | POST | Bestellung erstellen |
| `/orders/{order_id}` | GET | Bestelldetails |
| `/orders/status/{status}` | GET | Bestellungen nach Status |
| `/orders/{order_id}/fulfill` | POST | Fulfillment |
| `/stats` | GET | Statistiken |

## 🔧 Architektur

```
dropshipping_app/
├── core_amazon_api.py      # Amazon Integration
├── core_pricing_engine.py   # Preisberechnung
├── core_order_manager.py    # Bestellverwaltung
├── core_supplier_api.py     # Lieferanten Integration
├── main.py                  # FastAPI Server
├── dashboard.py             # Streamlit UI
├── requirements.txt         # Dependencies
└── .env                     # Konfiguration
```

## 💡 Demo-Modus

Die App läuft standardmäßig im Demo-Modus ohne echte API-Keys. Für Produktivbetrieb:

1. Amazon API Key eintragen
2. Supplier API Key eintragen
3. `.env` aktualisieren

## 📈 Roadmap

- [ ] Automatische Preisoptimierung
- [ ] Multi-Channel Support (eBay, Shopify)
- [ ] Advanced Analytics
- [ ] Automatische Reorder-Logik
- [ ] Email-Benachrichtigungen

## 🔐 Sicherheit

- Alle API-Keys in `.env` speichern
- `.env` nicht ins Repository einchecken
- CORS nur für vertrauenswürdige Domains aktivieren

## 📞 Support

Für Fragen oder Bugs: Siehe README.md im Hauptprojekt
