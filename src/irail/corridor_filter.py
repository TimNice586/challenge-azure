from typing import List, Dict


# Define the corridor stations for filtering
CORRIDOR_DESTINATIONS = ["Blankenberge"]  # trains leaving Gent-Sint-Pieters

def filter_corridor_trains(liveboard_json: dict, corridor_destinations=CORRIDOR_DESTINATIONS) -> List[Dict]:
    """
    Filter departures from a liveboard JSON to keep only corridor trains.
    """
    filtered = []
    
    departures = liveboard_json.get("departures", {}).get("departure", [])
    
    for dep in departures:
        direction = dep.get("direction")
        if direction in corridor_destinations:
            filtered.append({
                "vehicle": dep.get("vehicle"),
                "station": liveboard_json.get("station", {}).get("name"),
                "direction": direction,
                "time": dep.get("time"),
                "delay": dep.get("delay"),
                "platform": dep.get("platform")
            })
    
    return filtered

