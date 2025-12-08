# 🚀 KONTROLLZENTRUM - QUICK START

## 1️⃣ Setup (2 Minuten)

```powershell
cd C:\Users\Laptop\Kontrollzentrum-1
py -3.11 setup_production.py
```

Das Skript macht automatisch:
- ✅ `.env` erstellen
- ✅ Dependencies installieren
- ✅ API-Keys prüfen
- ✅ Tests ausführen
- ✅ Interaktives Menü

## 2️⃣ API-Keys eintragen

Öffne `.env` und fülle aus:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Stripe
STRIPE_API_KEY=sk_live_...

# PayPal
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...

# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Security
JWT_SECRET=dein-super-geheimes-passwort
```

## 3️⃣ Starten

**Option A: CLI (interaktiv)**
```powershell
py -3.11 main.py
```

**Option B: Team-Modus (alle Module automatisch)**
```powershell
py -3.11 main.py team
```

**Option C: API Gateway (http://localhost:8000)**
```powershell
py -3.11 main.py api
```

**Option D: Streamlit Dashboard**
```powershell
streamlit run main.py
```

**Option E: Health Check**
```powershell
py -3.11 main.py health
```

## 4️⃣ Neues Modul erstellen

1. Datei in `modules/` erstellen (z.B. `mein_modul.py`)
2. `run()`-Funktion schreiben:

```python
from core.key_check import require_keys

@require_keys
def run():
    return {"status": "ok", "message": "Mein Modul läuft!"}

def install():
    print("✅ Installiert")
```

3. Modul wird automatisch geladen!

## 5️⃣ Tests ausführen

```powershell
py -3.11 -m unittest discover tests -v
```

## 📁 Projektstruktur

```
Kontrollzentrum-1/
├── main.py                 # Haupt-Entry-Point
├── setup_production.py     # Setup-Wizard
├── requirements.txt        # Dependencies
├── .env                    # API-Keys (NICHT ins Git!)
├── .env.example            # Template
│
├── core/                   # Kern-Module
│   ├── key_check.py       # API-Key-Validierung
│   ├── api_gateway.py     # FastAPI
│   ├── zenith_controller.py # Streamlit
│   ├── health_monitor.py  # Monitoring
│   ├── database.py        # SQLite
│   └── rate_limiter.py    # Rate-Limiting
│
├── modules/               # Plug-and-Play Module
│   └── beispiel_modul.py
│
├── tests/                 # Unit-Tests
│   └── test_new_modules.py
│
└── logs/                  # Logs & Backups
```

## 🔑 Erforderliche API-Keys

| Key | Quelle | Zweck |
|-----|--------|-------|
| OPENAI_API_KEY | https://platform.openai.com | GPT-4, DALL-E, Whisper |
| STRIPE_API_KEY | https://dashboard.stripe.com | Payment Processing |
| PAYPAL_CLIENT_ID/SECRET | https://developer.paypal.com | PayPal Checkout |
| AWS_ACCESS_KEY_ID/SECRET | https://aws.amazon.com | S3, EC2, Lambda |
| JWT_SECRET | Beliebig | Token-Signierung |

## ⚠️ Wichtig

- **`.env` NIEMALS ins Git einchecken!**
- Alle Module müssen eine `run()`-Funktion haben
- API-Keys sind erforderlich für Produktivbetrieb
- Tests vor Deployment ausführen

## 🆘 Troubleshooting

**Fehler: "Fehlende Keys"**
→ `.env` prüfen und alle Keys eintragen

**Fehler: "Modul nicht gefunden"**
→ Datei in `modules/` muss `.py` sein und `run()` haben

**Fehler: "Dependencies fehlen"**
→ `py -3.11 -m pip install -r requirements.txt`

**API Gateway startet nicht**
→ Port 8000 ist belegt: `netstat -ano | findstr :8000`

---

**Viel Erfolg! 🚀**
