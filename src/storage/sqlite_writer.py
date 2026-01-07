import sqlite3
from pathlib import Path

DB_PATH = Path("data/departures.db")
SCHEMA_PATH = Path("src/storage/schema.sql")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())


def insert_departures(records: list[dict]):
    if not records:
        return

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT OR IGNORE INTO corridor_departures (
                timestamp,
                station_departure,
                vehicle,
                train_type,
                delay_seconds,
                platform,
                corridor
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    r["timestamp"],
                    r["station_departure"],
                    r["vehicle"],
                    r["train_type"],
                    r["delay_seconds"],
                    r["platform"],
                    r["corridor"],
                )
                for r in records
            ],
        )
        conn.commit()
