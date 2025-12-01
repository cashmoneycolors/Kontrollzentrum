# 🚀 Quick-Start Guide - Kontrollzentrum

## 1️⃣ **Projekt starten (3 Optionen)**

### Option A: CLI-Modus (Alle Module ausführen)
```bash
python main.py alle run
```
**Ergebnis:** 14/14 Module erfolgreich ✅

### Option B: Team-Modus (Installation + Ausführung)
```bash
python main.py team
```
**Ergebnis:** Log in `team_log.txt`

### Option C: Streamlit-Dashboard
```bash
streamlit run main.py
```
**Ergebnis:** Web-UI mit Sidebar-Navigation

---

## 2️⃣ **Roboter-Modus (Autonome Verwaltung)**
```bash
python mega_roboter_ki.py
```
**Menü:**
1. Struktur prüfen
2. Abhängigkeiten installieren
3. Module testen
4. API-Integration testen
5. Backup erstellen
6. API-Keys prüfen

---

## 3️⃣ **API-Server starten (FastAPI)**
```bash
python modules/ki_sideboard.py
```
**Endpoints:**
- `GET /health` - Health-Check
- `POST /openai_vision` - Vision API
- `POST /mathpix` - Math Recognition

**Test mit curl:**
```bash
curl http://localhost:8003/health
```

---

## 4️⃣ **Tests ausführen**
```bash
# Alle Tests
python -m unittest discover -s tests -p "test_*.py" -v

# Spezifische Test-Suite
python -m unittest tests.test_new_modules -v
```

---

## 5️⃣ **Produktive API-Keys eintragen**

Öffne `.env` und ersetze Test-Keys:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
STRIPE_API_KEY=sk_live_xxxxxxxxxxxxx
PAYPAL_CLIENT_ID=xxxxxxxxxxxxx
# ... weitere Keys
```

---

## 📊 **Verfügbare Module (14 Stück)**

| Modul | Funktion |
|-------|----------|
| beispiel_modul | Test-Modul |
| wetter_modul | Open-Meteo Integration |
| ki_integration_modul | KI-Integration |
| dropshipping_modul | Dropshipping-Logik |
| ki_modul | KI-Produktivmodul |
| grafik_design_modul | Grafik-Design |
| data_import | Daten-Import |
| nft_modul | NFT-Management |
| dashboard_modul | Visualisierung |
| payment | Stripe/PayPal |
| nft_manager | NFT-Minting |
| auto_distribute | eBay/Amazon Upload |
| self_heal | System Recovery |
| apikey_manager | Key-Verwaltung |

---

## 🔧 **Troubleshooting**

### Problem: "FEHLENDE API-KEYS"
**Lösung:** Trage alle Keys in `.env` ein
```bash
python -c "from core.key_check import check_all_keys; check_all_keys()"
```

### Problem: "ModuleNotFoundError"
**Lösung:** Installiere Dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Streamlit nicht gefunden"
**Lösung:** Installiere Streamlit
```bash
pip install streamlit
```

---

## 📝 **Nächste Schritte**

1. ✅ Projekt starten: `python main.py alle run`
2. ✅ Dashboard testen: `streamlit run main.py`
3. ✅ API testen: `python modules/ki_sideboard.py`
4. ⏳ Produktive Keys eintragen
5. ⏳ Weitere Module entwickeln

---

**Status: 🟢 PRODUKTIONSBEREIT**

*Letzte Aktualisierung: 2025-11-30*
