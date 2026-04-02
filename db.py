import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_listings (
            id       TEXT PRIMARY KEY,
            city     TEXT NOT NULL,
            source   TEXT NOT NULL,
            seen_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_seen(listing_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT 1 FROM seen_listings WHERE id = ?", (listing_id,)
    ).fetchone()
    conn.close()
    return row is not None


def mark_seen(listing_id: str, city: str, source: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO seen_listings (id, city, source) VALUES (?, ?, ?)",
        (listing_id, city, source)
    )
    conn.commit()
    conn.close()