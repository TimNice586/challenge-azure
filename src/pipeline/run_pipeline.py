from src.irail.liveboard import fetch_liveboard
from src.irail.corridors import CORRIDORS
from src.pipeline.corridor_filter import filter_corridor_departures
from src.pipeline.normalizer import normalize_departure
from src.storage.sqlite_writer import init_db, insert_departures
from src.storage.azure_writer import insert_departures_azure
from src.config.azure_sql import get_azure_conn_str
from src.reference.stations import init_stations_table, upsert_station, insert_station_manual
import pyodbc


def main():
    print("Pipeline booted\n")

    # 1. Initialize DB
    init_db()
    print("DB initialized")
    init_stations_table()

    # 2. Fetch raw liveboard data
    departures = fetch_liveboard("Gent-Sint-Pieters")
    print(f"\nFetched {len(departures)} departures:")
    for dep in departures[:5]:  # show only first 5 for readability
        print(dep)
    # when iterating departures
    for dep in departures:
        if "stationinfo" in dep:
            upsert_station(dep["stationinfo"])
    # insert origin station explicitly
    insert_station_manual(
        station_id="BE.NMBS.008892007",
        name="Ghent-Sint-Pieters",
        lat=51.035896,
        lon=3.710202)

    # 3. Filter only corridor departures
    corridor_departures = filter_corridor_departures(departures, CORRIDORS)
    print(f"\nFound {len(corridor_departures)} corridor trains:")
    for dep in corridor_departures:
        print(dep)
    

    # 4. Normalize for DB storage
    normalized = [normalize_departure(d) for d in corridor_departures]
    print("\nNormalized departures for DB:")
    for dep in normalized:
        print(dep)

    # 5. Persist to SQLite
    insert_departures(normalized)
    print("\nPipeline completed, departures inserted into SQLite DB")

    # 6. Persist to Azure
    # ---- TEMPORARILY DISABLED ----
    # conn_str = get_azure_conn_str()
    # with pyodbc.connect(conn_str) as conn:
    #   insert_departures_azure(normalized, conn)
    #   print("Departures inserted into Azure SQL DB")

if __name__ == "__main__":
    main()

