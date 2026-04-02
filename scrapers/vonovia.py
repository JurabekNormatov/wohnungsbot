import requests
from scrapers.base import BaseScraper

API_URL  = "https://www.vonovia.de/api/real-estate/list"
BASE_URL = "https://www.vonovia.de/zuhause-finden/immobilien"


class VonoviaScraper(BaseScraper):

    SOURCE = "Vonovia"
    CITY   = "hamburg"

    def get_listings(self) -> list[dict]:
        try:
            params = {
                "limit": 50,
                "rentType": "miete",
                "city": "Hamburg",
            }
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36"
                ),
                "Accept": "application/json",
                "Referer": "https://www.vonovia.de",
            }
            resp = requests.get(
                API_URL, params=params, headers=headers, timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[Vonovia] Fehler: {e}")
            return []

        results = []
        for item in data.get("results", []):
            try:
                uid     = item.get("wrk_id", "")
                title   = item.get("titel", "")
                strasse = item.get("strasse", "")
                plz     = item.get("plz", "")
                ort     = item.get("ort", "")
                address = f"{strasse}, {plz} {ort}"
                preis   = item.get("preis", 0)
                groesse = item.get("groesse", 0)
                zimmer  = item.get("anzahl_zimmer", 0)
                slug    = item.get("slug", uid)
                url     = f"{BASE_URL}/{slug}"

                if zimmer == 0 or groesse < 20:
                    continue

                results.append({
                    "id":            f"vonovia-{uid}",
                    "title":         title,
                    "address":       address,
                    "warmmiete":     f"{preis:,.2f} €".replace(",", ".").replace(".", ",", 1),
                    "warmmiete_num": float(preis),
                    "size":          f"{groesse} m²",
                    "groesse_num":   float(groesse),
                    "rooms":         str(zimmer),
                    "zimmer_num":    float(zimmer),
                    "url":           url,
                    "source":        self.SOURCE,
                    "city":          self.CITY,
                })
            except Exception as e:
                print(f"[Vonovia] Fehler bei Wohnung: {e}")
                continue

        return results


class VonoviaBerlinScraper(BaseScraper):

    SOURCE = "Vonovia"
    CITY   = "berlin"

    def get_listings(self) -> list[dict]:
        try:
            params = {
                "limit": 50,
                "rentType": "miete",
                "city": "Berlin",
            }
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36"
                ),
                "Accept": "application/json",
                "Referer": "https://www.vonovia.de",
            }
            resp = requests.get(
                API_URL, params=params, headers=headers, timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[Vonovia Berlin] Fehler: {e}")
            return []

        results = []
        for item in data.get("results", []):
            try:
                uid     = item.get("wrk_id", "")
                title   = item.get("titel", "")
                strasse = item.get("strasse", "")
                plz     = item.get("plz", "")
                ort     = item.get("ort", "")
                address = f"{strasse}, {plz} {ort}"
                preis   = item.get("preis", 0)
                groesse = item.get("groesse", 0)
                zimmer  = item.get("anzahl_zimmer", 0)
                slug    = item.get("slug", uid)
                url     = f"{BASE_URL}/{slug}"

                if zimmer == 0 or groesse < 20:
                    continue

                results.append({
                    "id":            f"vonovia-berlin-{uid}",
                    "title":         title,
                    "address":       address,
                    "warmmiete":     f"{preis:,.2f} €".replace(",", ".").replace(".", ",", 1),
                    "warmmiete_num": float(preis),
                    "size":          f"{groesse} m²",
                    "groesse_num":   float(groesse),
                    "rooms":         str(zimmer),
                    "zimmer_num":    float(zimmer),
                    "url":           url,
                    "source":        self.SOURCE,
                    "city":          self.CITY,
                })
            except Exception as e:
                print(f"[Vonovia Berlin] Fehler bei Wohnung: {e}")
                continue

        return results