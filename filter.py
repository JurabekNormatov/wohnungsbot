FILTERS = {
    "berlin": {
        "max_warmmiete": 1200,
        "min_zimmer": 1,
        "max_zimmer": 4,
        "min_groesse": 30,
    },
    "hamburg": {
        "max_warmmiete": 1300,
        "min_zimmer": 1,
        "max_zimmer": 4,
        "min_groesse": 30,
    },
}


def passes_filter(listing: dict, city: str) -> bool:
    f = FILTERS.get(city, {})

    warmmiete = listing.get("warmmiete_num")
    if warmmiete and f.get("max_warmmiete"):
        if warmmiete > f["max_warmmiete"]:
            return False

    zimmer = listing.get("zimmer_num")
    if zimmer:
        if f.get("min_zimmer") and zimmer < f["min_zimmer"]:
            return False
        if f.get("max_zimmer") and zimmer > f["max_zimmer"]:
            return False

    groesse = listing.get("groesse_num")
    if groesse and f.get("min_groesse"):
        if groesse < f["min_groesse"]:
            return False

    return True