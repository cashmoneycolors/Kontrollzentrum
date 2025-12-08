# GitHub Setup für Kontrollzentrum v5.0

## 1. Repository erstellen

```bash
# Auf GitHub.com:
# 1. Neues Repository: "kontrollzentrum"
# 2. Public oder Private
# 3. Keine README/License (wir haben schon eine)
```

## 2. Remote hinzufügen

```bash
git remote add origin https://github.com/USERNAME/kontrollzentrum.git
git branch -M main
```

## 3. Alle Dateien committen

```bash
git add .
git commit -m "🚀 Kontrollzentrum v5.0 - Production Ready"
git push -u origin main
```

## 4. GitHub Secrets setzen

Gehe zu: Settings → Secrets and variables → Actions

Füge hinzu:
- `OPENAI_API_KEY`
- `STRIPE_API_KEY`
- `PAYPAL_CLIENT_ID`
- `AWS_ACCESS_KEY_ID`

## 5. Deployment aktivieren

```bash
# GitHub Pages (optional)
# Settings → Pages → Deploy from branch: main /docs

# GitHub Actions (automatisch aktiv)
# Workflows laufen bei jedem Push
```

## 6. Branches schützen

Settings → Branches → Add rule:
- Branch name pattern: `main`
- Require pull request reviews
- Require status checks to pass

## 7. Fertig! 🎉

Dein Projekt ist jetzt auf GitHub und wird automatisch getestet!
