from scrapers.base import BaseScraper

BASE_URL = "https://www.howoge.de"
LIST_URL = (
    "https://www.howoge.de/immobiliensuche/wohnungssuche.html"
)


class HowogeScraper(BaseScraper):

    SOURCE = "HOWOGE"
    CITY   = "berlin"

    def get_listings(self) -> list[dict]:
        soup = self.fetch(LIST_URL)
        if not soup:
            return []

        results = []
        cards = soup.select("div.flat-single-grid-item")

        for card in cards:
            try:
                uid = card.get("data-uid", "")

                # Titel
                notice = card.select_one("div.notice")
                title = notice.get_text(strip=True) if notice else ""

                # URL + Adresse
                link_tag = card.select_one("a.flat-single--link")
                if not link_tag:
                    continue
                url     = BASE_URL + link_tag.get("href", "")
                address = link_tag.get_text(strip=True)

                # Preis, Größe, Zimmer
                data = card.select("div.flat-data span")
                warmmiete = data[0].get_text(strip=True) if len(data) > 0 else ""
                groesse   = data[1].get_text(strip=True) if len(data) > 1 else ""
                zimmer    = data[2].get_text(strip=True) if len(data) > 2 else ""

                results.append({
                    "id":       f"howoge-{uid}",
                    "title":    title,
                    "address":  address,
                    "warmmiete": warmmiete,
                    "warmmiete_num": self._parse_num(warmmiete),
                    "size":     groesse,
                    "groesse_num": self._parse_num(groesse),
                    "rooms":    zimmer,
                    "zimmer_num": self._parse_num(zimmer),
                    "url":      url,
                    "source":   self.SOURCE,
                    "city":     self.CITY,
                })

            except Exception as e:
                print(f"[HOWOGE] Fehler bei Karte: {e}")
                continue

        return results

    def _parse_num(self, text: str) -> float | None:
        try:
            cleaned = text.replace("€", "").replace("m²", "")
            cleaned = cleaned.replace(".", "").replace(",", ".")
            cleaned = cleaned.strip()
            return float(cleaned)
        except Exception:
            return None