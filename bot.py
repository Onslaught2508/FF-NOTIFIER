#!/usr/bin/env python3
import requests
import logging
import sys
import os
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "bot.log")

BC_API_URL = "https://de.store.square-enix-games.com/remote/v1/product-attributes/3473"

PRODUCTS = [
    {
        "id":      "ffr-ce-ps5",
        "name":    "FFR Collector's Edition PS5",
        "type":    "bc_api",
        "payload": {"product_id": "3473", "attribute[1004]": "1488", "attribute[1005]": "1491"},
        "url":     "https://de.store.square-enix-games.com/final-fantasy-resonance",
    },
    {
        "id":      "ffr-goods-box",
        "name":    "FFR Collector's Goods Box (ohne Spiel)",
        "type":    "keyword",
        "url":     "https://de.store.square-enix-games.com/final-fantasy-resonance-collector_s-edition-goods-box",
    },
]

NTFY_URL = os.environ.get("NTFY_URL", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}

RETRY_COUNT = 3
RETRY_DELAY = 5  # Sekunden zwischen Versuchen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def check_bc_api(payload):
    last_error = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.post(
                BC_API_URL,
                data={**payload, "action": "add", "qty[]": "1"},
                headers=HEADERS,
                timeout=15,
            )
            resp.raise_for_status()
            data        = resp.json().get("data", {})
            instock     = data.get("instock", False)
            stock       = data.get("stock", 0)
            purchasable = data.get("purchasable", False)
            msg         = data.get("purchasing_message") or data.get("stock_message") or ""
            if instock and purchasable and not msg:
                return "available", f"instock=true, stock={stock}"
            else:
                return "unavailable", f"instock={instock}, stock={stock}, msg='{msg}'"
        except Exception as e:
            last_error = e
            log.warning(f"  API-Fehler (Versuch {attempt}/{RETRY_COUNT}): {e}")
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY)
    log.error(f"  API dauerhaft nicht erreichbar nach {RETRY_COUNT} Versuchen.")
    return "error", str(last_error)


def check_keyword(url):
    last_error = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.get(url, headers={**HEADERS, "Accept": "text/html"}, timeout=15)
            resp.raise_for_status()
            text = resp.text.lower()
            if "derzeit nicht verfügbar" in text or "out of stock" in text:
                return "unavailable", "Nicht-verfuegbar-Text gefunden"
            if "in den warenkorb" in text or "btnatc" in text:
                return "available", "Warenkorb-Element gefunden"
            return "unknown", "kein eindeutiger Status"
        except Exception as e:
            last_error = e
            log.warning(f"  HTTP-Fehler (Versuch {attempt}/{RETRY_COUNT}): {e}")
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY)
    log.error(f"  Seite dauerhaft nicht erreichbar nach {RETRY_COUNT} Versuchen.")
    return "error", str(last_error)


def send_ntfy(title, message, priority="urgent", tags="white_check_mark,shopping"):
    if not NTFY_URL:
        log.warning("NTFY_URL nicht gesetzt – keine Benachrichtigung.")
        return
    try:
        r = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title":    title.encode("utf-8"),
                "Priority": priority,
                "Tags":     tags,
            },
            timeout=10,
        )
        r.raise_for_status()
        log.info(f"  ntfy gesendet: {title}")
    except Exception as e:
        log.error(f"  ntfy-Fehler: {e}")


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for p in PRODUCTS:
        if p["type"] == "bc_api":
            status, detail = check_bc_api(p["payload"])
        else:
            status, detail = check_keyword(p["url"])

        log.info(f"{p['name']}: {status} ({detail})")

        if status == "available":
            send_ntfy(
                title=f"VERFUEGBAR: {p['name']}",
                message=f"Jetzt kaufen!\nZeit: {now}\nURL:  {p['url']}",
            )

if __name__ == "__main__":
    main()
