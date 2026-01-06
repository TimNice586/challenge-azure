import requests


def fetch_liveboard(station_name: str) -> dict:
    """
    Fetch live departure board for a given station.
    """
    url = "https://api.irail.be/v1/liveboard/"
    params = {
        "station": station_name,
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status() #checks status code (200-299 is ok, 400-599 raises requests.exceptions.HTTPError) -> prevents silent failures

    return response.json()
