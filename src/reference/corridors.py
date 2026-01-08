import sqlite3


CORRIDORS = {
    "GHENT_BLANKENBERGE": {
        "from": "Ghent-Sint-Pieters",
        "to": "Blankenberge"
    }
}

DB_PATH = "data/trains.db"

def load_corridor_endpoints():
    """
    Returns:
    {
        corridor_name: {
            "from": {"name": ..., "lat": ..., "lon": ...},
            "to":   {"name": ..., "lat": ..., "lon": ...}
        }
    }
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    resolved = {}

    for corridor, cfg in CORRIDORS.items():
        cur.execute(
            """
            SELECT name, lat, lon
            FROM stations
            WHERE name = ?
            """,
            (cfg["from"],)
        )
        from_station = cur.fetchone()

        cur.execute(
            """
            SELECT name, lat, lon
            FROM stations
            WHERE name = ?
            """,
            (cfg["to"],)
        )
        to_station = cur.fetchone()

        if not from_station or not to_station:
            raise ValueError(f"Station not found for corridor {corridor}")

        resolved[corridor] = {
            "from": {
                "name": from_station[0],
                "lat": from_station[1],
                "lon": from_station[2],
            },
            "to": {
                "name": to_station[0],
                "lat": to_station[1],
                "lon": to_station[2],
            },
        }

    conn.close()
    return resolved
