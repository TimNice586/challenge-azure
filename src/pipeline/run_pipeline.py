from src.irail.liveboard import fetch_liveboard
from src.irail.corridors import CORRIDORS
from src.pipeline.corridor_filter import filter_corridor_departures
from src.pipeline.normalizer import normalize_departure
from src.storage.sqlite_writer import init_db, insert_departures
from src.storage.azure_writer import insert_departures_azure

def main():
    print("Pipeline booted\n")

    # 1. Initialize DB
    init_db()
    print("DB initialized")

    # 2. Fetch raw liveboard data
    departures = fetch_liveboard("Gent-Sint-Pieters")
    print(f"\nFetched {len(departures)} departures:")
    for dep in departures[:5]:  # show only first 5 for readability
        print(dep)

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
    insert_departures_azure(normalized, conn_str)
    print("Departures inserted into Azure SQL DB")

if __name__ == "__main__":
    main()

