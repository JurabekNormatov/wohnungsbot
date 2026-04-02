from scrapers.base import BaseScraper

BASE_URL = "https://www.wbm.de"
LIST_URL = "https://www.wbm.de/wohnungen-berlin/angebote/"


class WbmScraper(BaseScraper):

    SOURCE = "WBM"
    CITY   = "berlin"

    def get_listings(self) -> list[dict]:
        soup = self.fetch(LIST_URL)
        if not soup:
            return []

        results = []
        cards = soup.select("div.openimmo-search-list-item")

        for card in cards:
            try:
                uid = card.get("data-uid", "")

                # Titel
                title_tag = card.select_one("b")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # URL
                link_tag = card.select_one("a[href*='/wohnungen-berlin/']")
                if not link_tag:
                    continue
                url = BASE_URL + link_tag.get("href", "")

                # Adresse
                tooltip = card.select_one(f"div[id*='{uid}']")
                if tooltip:
                    lines = [t.strip() for t in tooltip.get_text().splitlines() if t.strip()]
                    address = " ".join(lines[1:3]) if len(lines) >= 3 else ""
                else:
                    address = ""

                # Miete, Zimmer, Größe
                rent_tag  = card.select_one("div.main-property-value.main-property-rent")
                rooms_tag = card.select_one("div.main-property-value.main-property-rooms")
                size_tag  = card.select_one("div.main-property-value.main-property-size")

                warmmiete = rent_tag.get_text(strip=True)  if rent_tag  else ""
                zimmer    = rooms_tag.get_text(strip=True) if rooms_tag else ""
                groesse   = size_tag.get_text(strip=True)  if size_tag  else ""

                results.append({
                    "id":            f"wbm-{uid}",
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
                print(f"[WBM] Fehler: {e}")
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