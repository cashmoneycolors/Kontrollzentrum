# 🎬 Demo-Anleitung

## Schritt 1: Installation & Start

```bash
# Terminal 1 - API Server starten
cd dropshipping_app
pip install -r requirements.txt
python main.py
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

```bash
# Terminal 2 - Dashboard starten
streamlit run dashboard.py
```

**Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## Schritt 2: API testen (curl/Postman)

### Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok", "service": "dropshipping-api"}
```

### Produkte suchen
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Wireless Headphones", "category": "Elektronik"}'
```

**Response:**
```json
{
  "products": [
    {
      "asin": "B001",
      "title": "Premium Wireless Headphones - 100% Original",
      "price": 29.99,
      "rating": 4.8,
      "supplier": "alibaba",
      "supplier_price": 8.50,
      "selling_price": 34.99,
      "profit": 23.34,
      "margin": 33.3
    }
  ]
}
```

### Bestellung erstellen
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "customer@example.com",
    "items": [{"asin": "B001", "qty": 1}],
    "total": 34.99
  }'
```

**Response:**
```json
{
  "order_id": "ORD-1000",
  "customer_email": "customer@example.com",
  "items": [{"asin": "B001", "qty": 1}],
  "total": 34.99,
  "status": "pending",
  "created_at": "2025-01-15T10:30:00",
  "tracking": null
}
```

### Statistiken abrufen
```bash
curl http://localhost:8000/stats
```

**Response:**
```json
{
  "pending_orders": 1,
  "shipped_orders": 0,
  "delivered_orders": 0,
  "total_orders": 1
}
```

---

## Schritt 3: Dashboard Demo

### Tab 1: Produktsuche
1. Öffne http://localhost:8501
2. Gib "Wireless Headphones" ein
3. Klicke "🔍 Suchen"
4. Sehe Ergebnisse mit Preisen, Lieferanten und Gewinn

### Tab 2: Statistiken
- Zeigt Live-Daten von API
- Aktualisiert sich automatisch

### Tab 3: Bestellverwaltung
1. Gib Kundenmail ein
2. Erstelle Bestellung
3. Suche Bestellung nach ID

### Tab 4: Profitrechner
1. Gib Lieferantenpreis ein
2. Stelle Gewinnmarge ein
3. Sehe berechnete Verkaufspreise

---

## Schritt 4: Automatische Fulfillment

```bash
# Bestellung als versendet markieren
curl -X POST "http://localhost:8000/orders/ORD-1000/fulfill?supplier_tracking=TRACK-ALIBABA-12345"
```

**Response:**
```json
{
  "order_id": "ORD-1000",
  "status": "shipped",
  "tracking": "TRACK-ALIBABA-12345",
  ...
}
```

---

## Demo-Szenarien

### Szenario 1: Schnelle Produktsuche
**Zeit:** 2 Min
1. Starte API & Dashboard
2. Suche "Smartphone Case"
3. Sehe Preise, Lieferanten, Gewinn
4. Berechne Profitabilität

### Szenario 2: Bestellverwaltung
**Zeit:** 3 Min
1. Erstelle Bestellung
2. Markiere als versendet
3. Verfolge Status
4. Sehe Statistiken

### Szenario 3: Preisoptimierung
**Zeit:** 2 Min
1. Nutze Profitrechner
2. Teste verschiedene Margen
3. Finde optimalen Preis
4. Vergleiche Lieferanten

---

## Troubleshooting

### API startet nicht
```bash
# Port 8000 bereits in Verwendung?
netstat -ano | findstr :8000
# Oder anderen Port nutzen:
python main.py --port 8001
```

### Dashboard verbindet sich nicht
```bash
# Stelle sicher, dass API läuft
curl http://localhost:8000/health
```

### Keine Produkte gefunden
- Demo-Modus ist aktiv (kein API-Key nötig)
- Versuche andere Suchbegriffe
- Prüfe Logs im Terminal

---

## Performance-Metriken

| Metrik | Wert |
|--------|------|
| API Response Time | ~100ms |
| Dashboard Load | ~1.5s |
| Produktsuche | ~200ms |
| Bestellung erstellen | ~50ms |

---

## Nächste Schritte

Nach Demo:
1. ✅ Echte API-Keys in `.env` eintragen
2. ✅ Produktivdaten laden
3. ✅ Automatische Preisoptimierung aktivieren
4. ✅ Multi-Channel Integration starten

**Geschätzte Zeit bis Produktivbetrieb:** 2-3 Tage
