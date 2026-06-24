# FF-NOTIFIER 🎮

Automatischer Verfügbarkeits-Checker für **Final Fantasy Resonance** Collector's Edition und Goods Box im Square Enix Store.

## Was macht dieser Bot?

- Prüft alle 5 Minuten die Produktverfügbarkeit im Square Enix Store
- Sendet eine Push-Benachrichtigung via [ntfy](https://ntfy.sh), sobald ein Produkt verfügbar ist
- Läuft vollautomatisch über GitHub Actions – kein eigener Server nötig

## Überwachte Produkte

| Produkt | URL |
|---|---|
| Final Fantasy Resonance – Collector's Edition (PS5) | [Link](https://de.store.square-enix-games.com/final-fantasy-resonance) |
| Final Fantasy Resonance – Collector's Goods Box (ohne Spiel) | [Link](https://de.store.square-enix-games.com/final-fantasy-resonance-collector_s-edition-goods-box) |

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
