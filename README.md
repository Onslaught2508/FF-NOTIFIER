# FF-NOTIFIER 🎮

Automatischer Verfügbarkeits-Checker für **Final Fantasy Rebirth** Collector's Edition und Goods Box im Square Enix Store.

## Was macht dieser Bot?

- Prüft alle 5 Minuten die Produktverfügbarkeit im Square Enix Store
- Sendet eine Push-Benachrichtigung via [ntfy](https://ntfy.sh), sobald ein Produkt verfügbar ist
- Läuft vollautomatisch über GitHub Actions – kein eigener Server nötig

## Überwachte Produkte

| Produkt | URL |
|---|---|
| Final Fantasy VII Rebirth – Collector's Edition (PS5) | [Link](https://store.eu.square-enix-games.com/de_DE/product/870382/final-fantasy-vii-rebirth-collectors-edition-ps5) |
| Final Fantasy VII Rebirth – Collector's Goods Box (ohne Spiel) | [Link](https://store.eu.square-enix-games.com/de_DE/product/870388/final-fantasy-vii-rebirth-collectors-goods-box-ohne-spiel) |

## Technischer Aufbau

- **Sprache:** Python 3.11
- **Plattform:** GitHub Actions (kostenlos, 24/7)
- **Benachrichtigung:** [ntfy.sh](https://ntfy.sh) (Push auf iOS/Android/Desktop)
- **Intervall:** alle 5 Minuten via Cron-Job

## Konfiguration

Der ntfy-Kanal wird als **GitHub Actions Secret** hinterlegt und ist nicht im Code sichtbar:

| Secret | Beschreibung |
|---|---|
| `NTFY_URL` | Vollständige ntfy-URL, z. B. `https://ntfy.sh/dein-kanal` |

→ Settings → Secrets and variables → Actions → New repository secret

## Lokale Nutzung

```bash
pip install requests
export NTFY_URL="https://ntfy.sh/dein-kanal"
python bot.py
```

## Lizenz

MIT
