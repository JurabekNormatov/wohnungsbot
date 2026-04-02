import requests
import time
from config import (
    BERLIN_BOT_TOKEN, BERLIN_CHAT_ID,
    HAMBURG_BOT_TOKEN, HAMBURG_CHAT_ID
)


def _send(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=10)
    if not resp.ok:
        print(f"[FEHLER] {resp.status_code}: {resp.text}")

    time.sleep(1)
    
def _format(listing: dict) -> str:
    lines = [
        f"🏠 <b>{listing.get('title', 'Neue Wohnung')}</b>",
        f"📍 {listing.get('address', 'Adresse unbekannt')}",
    ]
    if listing.get("rooms"):
        lines.append(f"🚪 Zimmer: {listing['rooms']}")
    if listing.get("size"):
        lines.append(f"📐 Größe: {listing['size']}")
    if listing.get("warmmiete"):
        lines.append(f"💶 Warmmiete: {listing['warmmiete']}")
    if listing.get("kaltmiete"):
        lines.append(f"💶 Kaltmiete: {listing['kaltmiete']}")
    lines.append(f"🔗 <a href=\"{listing['url']}\">Zur Anzeige → {listing.get('source', '')}</a>")
    return "\n".join(lines)


def send_berlin(listing: dict):
    _send(BERLIN_BOT_TOKEN, BERLIN_CHAT_ID, _format(listing))


def send_hamburg(listing: dict):
    _send(HAMBURG_BOT_TOKEN, HAMBURG_CHAT_ID, _format(listing))