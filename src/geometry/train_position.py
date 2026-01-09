import sqlite3
import time
from shapely.geometry import LineString


DB_PATH = "data/railway.db"


def get_active_trains(conn):
    """
    Get trains that have future stops
    """
    now = int(time.time())
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT train_id
        FROM train_stops
        WHERE scheduled_departure <= ?
    """, (now,))

    return [row[0] for row in cur.fetchall()]


def get_train_stops(conn, train_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT
            station_id,
            scheduled_departure,
            delay
        FROM train_stops
        WHERE train_id = ?
        ORDER BY scheduled_departure
    """, (train_id,))

    return cur.fetchall()


def get_station_coords(conn, station_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT lat, lon
        FROM stations
        WHERE station_id = ?
    """, (station_id,))
    return cur.fetchone()


def interpolate_position(line, progress):
    if progress <= 0:
        return line.coords[0]
    if progress >= 1:
        return line.coords[-1]
    return line.interpolate(progress, normalized=True).coords[0]


def compute_train_position(train_id):
    conn = sqlite3.connect(DB_PATH)
    stops = get_train_stops(conn, train_id)

    if len(stops) < 2:
        return None

    now = int(time.time())

    for i in range(len(stops) - 1):
        station_a, time_a, _ = stops[i]
        station_b, time_b, _ = stops[i + 1]

        if time_a <= now <= time_b:
            coords_a = get_station_coords(conn, station_a)
            coords_b = get_station_coords(conn, station_b)

            if not coords_a or not coords_b:
                return None

            line = LineString([
                (coords_a[1], coords_a[0]),
                (coords_b[1], coords_b[0])
            ])

            progress = (now - time_a) / (time_b - time_a)
            lon, lat = interpolate_position(line, progress)

            return {
                "train_id": train_id,
                "lat": lat,
                "lon": lon
            }

    return None

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    trains = get_active_trains(conn)
    conn.close()

    for t in trains[:3]:
        print(compute_train_position(t))