import json
from scrapers.base import BaseScraper

BASE_URL = "https://www.kleinanzeigen.de"
LIST_URL = "https://www.kleinanzeigen.de/s-wohnung-mieten/hamburg/anzeige:angebote/seite:1/c203l9409"


class KleinanzeigenHamburgScraper(BaseScraper):

    SOURCE = "Kleinanzeigen"
    CITY   = "hamburg"

    def get_listings(self) -> list[dict]:
        soup = self.fetch(LIST_URL)
        if not soup:
            return []

        results = []
        articles = soup.select("article.aditem")

        for article in articles:
            try:
                uid      = article.get("data-adid", "")
                href     = article.get("data-href", "")
                url      = BASE_URL + href

                # Titel und Beschreibung aus JSON-LD
                script = article.select_one("script[type='application/ld+json']")
                if not script:
                    continue
                data  = json.loads(script.string)
                title = data.get("title", "")

                # Adresse
                address_tag = article.select_one("div.aditem-main--top--left")
                address = address_tag.get_text(strip=True) if address_tag else ""

                # Preis
                price_tag = article.select_one("p.aditem-main--middle--price-shipping--price")
                warmmiete = price_tag.get_text(strip=True).split("€")[0].strip() + " €" if price_tag else ""

                results.append({
                    "id":            f"kleinanzeigen-{uid}",
                    "title":         title,
                    "address":       address,
                    "warmmiete":     warmmiete,
                    "warmmiete_num": self._parse_num(warmmiete),
                    "size":          "",
                    "groesse_num":   None,
                    "rooms":         "",
                    "zimmer_num":    None,
                    "url":           url,
                    "source":        self.SOURCE,
                    "city":          self.CITY,
                })

            except Exception as e:
                print(f"[Kleinanzeigen] Fehler: {e}")
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