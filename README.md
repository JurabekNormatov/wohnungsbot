# Wohnungsbot

A Telegram bot that scrapes apartment listings from Berlin and Hamburg housing companies and posts new listings to Telegram channels automatically.

## What it does

- Scrapes WBM, DEGEWO, and Vonovia (Berlin) every 15 minutes
- Scrapes Vonovia (Hamburg) every 15 minutes
- Filters listings by price, size, and number of rooms
- Posts new listings to separate Telegram channels for Berlin and Hamburg
- Prevents duplicate posts using SQLite

## Tech Stack

- Python 3.13
- BeautifulSoup4 — HTML parsing
- Requests — HTTP calls
- SQLite — duplicate tracking
- Telegram Bot API — notifications
- GitHub Actions — automated scheduling

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:
```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and fill in your tokens:
```bash
   cp .env.example .env
```
4. Run manually:
```bash
   python3 main.py
```

## Automated runs

The bot runs automatically every 15 minutes via GitHub Actions.
Tokens are stored as GitHub Secrets — never in the code.

## Sources

| City | Source |
|------|--------|
| Berlin | WBM, DEGEWO, Vonovia |
| Hamburg | Vonovia |

## Author

Jurabek Normatov
