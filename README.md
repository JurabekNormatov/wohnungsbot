# 🏠 Wohnungsbot Berlin & Hamburg

Ein automatischer Telegram-Bot der Berliner und Hamburger Wohnungsportale durchsucht und neue Angebote sofort per Nachricht versendet — bevor sie auf großen Portalen erscheinen.

## 📊 Ergebnisse

- 40+ aktive Nutzer im Telegram-Kanal (Berlin)
- Eine Nutzerin fand nach 3 Jahren erfolgloser Suche innerhalb von einer Woche eine Wohnung — 1-Zimmer-Wohnung in Berlin für 360 €/Monat über eine Wohnungsgenossenschaft

## 🎯 Problem

Günstige Wohnungen bei Berliner Wohnungsgenossenschaften (WBM, Degewo, Vonovia) sind innerhalb von Stunden vergeben. Wer nicht sofort reagiert, hat keine Chance. Manuelle Kontrolle mehrerer Portale täglich ist zeitaufwendig und fehleranfällig.

## 💡 Lösung

Der Bot scraped automatisch mehrere Portale, filtert nach definierten Kriterien und sendet neue Angebote sofort in einen Telegram-Kanal — in Echtzeit, bevor die meisten Nutzer überhaupt von der Wohnung wissen.

## 🔧 Tech Stack

- Python 3.13
- BeautifulSoup4 — HTML-Parsing der Wohnungsportale
- Requests — HTTP-Scraping mit Anti-Bot-Headers
- SQLite — Duplikat-Erkennung (bereits gesehene Angebote)
- Telegram Bot API — Nachrichtenversand via requests
- dotenv — sichere Konfiguration über Umgebungsvariablen
- GitHub Actions — automatischer Betrieb alle 15 Minuten

## 🏗️ Architektur
```
wohnungsbot/
├── main.py              # Hauptprogramm — orchestriert alle Scraper
├── bot.py               # Telegram-Versand für Berlin und Hamburg
├── db.py                # SQLite — Duplikat-Erkennung
├── filter.py            # Filterlogik (Preis, Zimmer, Größe)
├── config.py            # Konfiguration
├── scrapers/
│   ├── base.py          # Basis-Scraper mit HTTP-Client
│   ├── wbm.py           # WBM Berlin
│   ├── degewo.py        # Degewo Berlin
│   ├── vonovia.py       # Vonovia Berlin & Hamburg
│   ├── howoge.py        # HOWOGE Berlin (in Entwicklung)
│   └── kleinanzeigen_hamburg.py  # Kleinanzeigen Hamburg
└── .env.example         # Konfigurationsvorlage
```

## ⚙️ Features

- 5 Scraper — WBM, Degewo, Vonovia, HOWOGE, Kleinanzeigen Hamburg
- Duplikat-Schutz — SQLite-Datenbank verhindert doppelte Benachrichtigungen
- Intelligenter Filter — konfigurierbar nach Warmmiete, Zimmeranzahl, Größe pro Stadt
- Zwei Kanäle — Berlin und Hamburg werden separat beliefert
- Robustes Fehlerhandling — einzelne Scraper-Fehler stoppen nicht den gesamten Lauf
- Anti-Bot-Headers — realistischer Browser-User-Agent
- GitHub Actions — läuft automatisch alle 15 Minuten ohne eigenen Server

## 🔍 Filterbeispiel
```python
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
```

## 🚀 Installation
```bash
git clone https://github.com/JurabekNormatov/wohnungsbot
cd wohnungsbot
pip install -r requirements.txt
cp .env.example .env
# .env mit eigenen Telegram-Tokens befüllen
python main.py
```

## 🔐 Konfiguration (.env)
```env
BERLIN_BOT_TOKEN=dein_token
BERLIN_CHAT_ID=deine_chat_id
HAMBURG_BOT_TOKEN=dein_token
HAMBURG_CHAT_ID=deine_chat_id
```

## 📈 Geplante Erweiterungen

- [x] GitHub Actions — automatischer Betrieb alle 15 Minuten ✓
- [ ] Weitere Portale: Gewobag, Saga Hamburg
- [ ] Web-Interface zur Filterkonfiguration
- [ ] Statistiken: Angebote pro Tag, durchschnittliche Preise

## 👨‍💻 Entwickler

Jurabek Normatov — Junior Java/Python Developer
github.com/JurabekNormatov