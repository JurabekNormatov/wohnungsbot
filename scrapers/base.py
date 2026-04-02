import time
import requests
from bs4 import BeautifulSoup
from config import REQUEST_TIMEOUT, SLEEP_BETWEEN

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "de-DE,de;q=0.9",
}


class BaseScraper:

    SOURCE = "Unbekannt"
    CITY   = "Unbekannt"

    def fetch(self, url: str) -> BeautifulSoup | None:
        try:
            time.sleep(SLEEP_BETWEEN)
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"[{self.SOURCE}] Fehler: {e}")
            return None

    def get_listings(self) -> list[dict]:
        raise NotImplementedError