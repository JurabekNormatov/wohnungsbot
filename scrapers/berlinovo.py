from scrapers.base import BaseScraper

BASE_URL = "https://www.berlinovo.de"
URLS = [
    "https://www.berlinovo.de/de/wohnungen/suche",
    "https://www.berlinovo.de/de/apartments/suche",
]


class BerlinovoScraper(BaseScraper):

    SOURCE = "Berlinovo"
    CITY   = "berlin"

    def get_listings(self) -> list[dict]:
        results = []

        for list_url in URLS:
            soup = self.fetch(list_url)
            if not soup:
                continue

            teasers = soup.select("div.teaser")

            for teaser in teasers:
                try:
                    # URL und Titel — letzten Link nehmen (hat den Text)
                    links = teaser.select("a[href*='/wohnung-id/'], a[href*='/de/apartments/']")
                    link  = links[-1] if links else None
                    if not link:
                        continue
                    url   = BASE_URL + link.get("href", "")
                    title = link.get_text(strip=True)
                    uid   = link.get("href", "").strip("/").replace("/", "-")

                    # Kategorie
                    cat_tag   = teaser.select_one("div.field--name-field-real-estate-category div.field__item")
                    kategorie = cat_tag.get_text(strip=True) if cat_tag else ""

                    # Adresse
                    strasse = teaser.select_one("span.address-line1")
                    plz     = teaser.select_one("span.postal-code")
                    ort     = teaser.select_one("span.locality")
                    address = ""
                    if strasse and plz and ort:
                        address = f"{strasse.get_text(strip=True)}, {plz.get_text(strip=True)} {ort.get_text(strip=True)}"

                    # Warmmiete
                    rent_tag  = teaser.select_one("div.field--name-field-total-rent div.field__item")
                    warmmiete = rent_tag.get_text(strip=True) if rent_tag else ""

                    # Zimmer
                    rooms_tag = teaser.select_one("div.field--name-field-rooms div.field__item")
                    zimmer    = rooms_tag.get("content", "") if rooms_tag else ""

                    # Verfügbar ab
                    date_tag   = teaser.select_one("time.datetime")
                    verfuegbar = date_tag.get_text(strip=True) if date_tag else ""

                    # Titel mit Kategorie
                    if kategorie:
                        full_title = f"{title} [{kategorie}]"
                    else:
                        full_title = title

                    results.append({
                        "id":            f"berlinovo-{uid}",
                        "title":         full_title,
                        "address":       address,
                        "warmmiete":     warmmiete,
                        "warmmiete_num": self._parse_num(warmmiete),
                        "size":          "",
                        "groesse_num":   None,
                        "rooms":         zimmer,
                        "zimmer_num":    self._parse_num(zimmer),
                        "verfuegbar":    verfuegbar,
                        "url":           url,
                        "source":        self.SOURCE,
                        "city":          self.CITY,
                    })

                except Exception as e:
                    print(f"[Berlinovo] Fehler: {e}")
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