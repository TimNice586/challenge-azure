import sqlite3

DB_PATH = "data/trains.db"


def init_stations_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                station_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL
            )
        """)
        conn.commit()

def insert_station_manual(station_id: str, name: str, lat: float, lon: float):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO stations (station_id, name, lat, lon)
            VALUES (?, ?, ?, ?)
        """, (station_id, name, lat, lon))
        conn.commit()

def upsert_station(stationinfo: dict):
    """
    stationinfo comes directly from iRail API
    """
    station_id = stationinfo["id"]
    name = stationinfo["standardname"]
    lat = float(stationinfo["locationY"])
    lon = float(stationinfo["locationX"])

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO stations (station_id, name, lat, lon)
            VALUES (?, ?, ?, ?)
        """, (station_id, name, lat, lon))
        conn.commit()


def get_station_coords(name: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
            SELECT lat, lon
            FROM stations
            WHERE name = ?
        """, (name,))
        row = cur.fetchone()
        return row if row else None
