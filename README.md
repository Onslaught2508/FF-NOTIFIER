# FF Availability Bot

Automatischer Verfügbarkeits-Check für ausgewählte Produkte im Square Enix Store (DE).  
Bei Verfügbarkeit kommt eine Push-Benachrichtigung via [ntfy](https://ntfy.sh).

## Überwachte Produkte

Konfiguriert in `products.json`:

| Produkt | Methode |
|---|---|
| FFR Collector's Edition PS5 | BigCommerce API |
| FFR Collector's Goods Box (ohne Spiel) | Keyword-Scan |

## Funktionsweise

- GitHub Actions prüft alle **5 Minuten** die Verfügbarkeit
- Bei Verfügbarkeit → ntfy-Benachrichtigung mit `priority: urgent`
- Bei dauerhaftem Ausfall aller Checks → ntfy-Benachrichtigung mit `priority: high`
- Täglich um **10:00 Uhr MESZ** (08:00 UTC) → stiller Heartbeat-Check via ntfy
- Netzwerkfehler werden bis zu **3× wiederholt** (5s Pause) bevor ein Fehler gemeldet wird
- Hängende Jobs werden nach **2 Minuten** automatisch abgebrochen

## Projektstruktur

```
FF-NOTIFIER/
├── .github/
│   └── workflows/
│       ├── check.yml          # Produktcheck alle 5 Minuten
│       └── heartbeat.yml      # Täglicher Lebenszeichen-Check
├── bot.py                     # Hauptskript
├── products.json              # Produktkonfiguration
└── README.md
```

## Konfiguration

### Neues Produkt hinzufügen

`products.json` editieren – `bot.py` bleibt unverändert.

**Typ `bc_api`** – für BigCommerce-API-Produkte:
```json
{
  "id":      "mein-produkt",
  "name":    "Produktname",
  "type":    "bc_api",
  "payload": {
    "product_id":      "1234",
    "attribute[1004]": "5678"
  },
  "url": "https://de.store.square-enix-games.com/..."
}
```

**Typ `keyword`** – für einfache Seiten ohne API:
```json
{
  "id":   "mein-produkt",
  "name": "Produktname",
  "type": "keyword",
  "url":  "https://de.store.square-enix-games.com/..."
}
```

### GitHub Secret

| Secret | Inhalt |
|---|---|
| `NTFY_URL` | Vollständige ntfy-URL, z. B. `https://ntfy.sh/mein-topic` |

Einzutragen unter: **Settings → Secrets and variables → Actions → New repository secret**

## Benachrichtigungen

| Ereignis | Titel | Priority |
|---|---|---|
| Produkt verfügbar | `VERFUEGBAR: <Name>` | `urgent` |
| Alle Checks fehlgeschlagen | `⚠️ Bot-Fehler: Alle Checks fehlgeschlagen` | `high` |
| Täglicher Heartbeat | `FF Bot läuft` | `low` |

## Lokaler Test

```bash
pip install requests
export NTFY_URL="https://ntfy.sh/mein-topic"
python bot.py
```

## Lizenz

MIT
