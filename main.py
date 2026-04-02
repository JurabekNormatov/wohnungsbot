from db import init_db, is_seen, mark_seen
from filter import passes_filter
from bot import send_berlin, send_hamburg
from scrapers.wbm import WbmScraper
from scrapers.degewo import DegewoScraper
from scrapers.vonovia import VonoviaScraper
from scrapers.vonovia import VonoviaScraper, VonoviaBerlinScraper
from scrapers.kleinanzeigen_hamburg import KleinanzeigenHamburgScraper


def run():
    init_db()
    scrapers = [
        WbmScraper(),
        DegewoScraper(),
        VonoviaBerlinScraper(),
        VonoviaScraper(),
        KleinanzeigenHamburgScraper(),
    ]

    for scraper in scrapers:
        print(f"[{scraper.SOURCE}] Scraping...")
        listings = scraper.get_listings()
        print(f"[{scraper.SOURCE}] {len(listings)} Wohnungen gefunden")

        for listing in listings:
            if is_seen(listing["id"]):
                continue

            if not passes_filter(listing, listing["city"]):
                print(f"  Gefiltert: {listing['title']}")
                continue

            if listing["city"] == "berlin":
                send_berlin(listing)
            elif listing["city"] == "hamburg":
                send_hamburg(listing)

            mark_seen(listing["id"], listing["city"], listing["source"])
            print(f"  Gepostet: {listing['title']}")


if __name__ == "__main__":
    run()