import requests
from typing import List, Dict

def fetch_liveboard(station_name: str) -> List[Dict]:
    """
    Fetch live departure board for a given station.
    Returns a list of departure dictionaries.
    """
    url = "https://api.irail.be/v1/liveboard/"
    params = {
        "station": station_name,
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error if the request failed

    data = response.json()

    # Ensure departures exist
    departures = data.get("departures", {}).get("departure", [])

    if not departures:
        print(f"No departures found for station: {station_name}")

    return departures
