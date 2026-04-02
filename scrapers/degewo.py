import re
from scrapers.base import BaseScraper

BASE_URL = "https://www.degewo.de"
LIST_URL = "https://www.degewo.de/immosuche"


class DegewoScraper(BaseScraper):

    SOURCE = "DEGEWO"
    CITY   = "berlin"

    def get_listings(self) -> list[dict]:
        soup = self.fetch(LIST_URL)
        if not soup:
            return []

        results = []
        cards = soup.select("div.article-list__content")

        for card in cards:
            try:
                # UID
                uid_tag = card.select_one("div[data-openimmo-bookmark-item-uid]")
                if not uid_tag:
                    continue
                uid = uid_tag.get("data-openimmo-bookmark-item-uid", "")

                # Titel
                title_tag = card.select_one("h2.article__title")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # URL aus Titel generieren
                url = f"{BASE_URL}/immosuche/details/{self._slugify(title)}"

                # Adresse
                meta_tag = card.select_one("span.article__meta")
                address = meta_tag.get_text(strip=True) if meta_tag else ""

                # Warmmiete
                price_tag = card.select_one("div.article__price-tag span.price")
                warmmiete = price_tag.get_text(strip=True) if price_tag else ""

                # Zimmer und Größe
                props = card.select("ul.article__properties li span.text")
                zimmer  = ""
                groesse = ""
                for prop in props:
                    text = prop.get_text(strip=True)
                    if "Zimmer" in text:
                        zimmer = text.replace("Zimmer", "").strip()
                    elif "m²" in text:
                        groesse = text

                results.append({
                    "id":            f"degewo-{uid}",
                    "title":         title,
                    "address":       address,
                    "warmmiete":     warmmiete,
                    "warmmiete_num": self._parse_num(warmmiete),
                    "size":          groesse,
                    "groesse_num":   self._parse_num(groesse),
                    "rooms":         zimmer,
                    "zimmer_num":    self._parse_num(zimmer),
                    "url":           url,
                    "source":        self.SOURCE,
                    "city":          self.CITY,
                })

            except Exception as e:
                print(f"[DEGEWO] Fehler: {e}")
                continue

        return results

    def _slugify(self, text: str) -> str:
        text = text.lower()
        text = text.replace("ä", "ae").replace("ö", "oe")
        text = text.replace("ü", "ue").replace("ß", "ss")
        text = text.replace("é", "e").replace("è", "e")
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = text.strip('-')
        return text

    def _parse_num(self, text: str) -> float | None:
        try:
            cleaned = text.replace("€", "").replace("m²", "")
            cleaned = cleaned.replace(".", "").replace(",", ".")
            cleaned = cleaned.strip()
            return float(cleaned)
        except Exception:
            return None