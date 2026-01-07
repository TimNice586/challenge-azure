from typing import Dict, List


def filter_corridor_departures(
    departures: List[dict],
    corridors: Dict[str, List[str]]
) -> List[dict]:
    """
    Filters liveboard departures to keep only those
    that belong to one of the defined corridors.

    A departure belongs to a corridor if its destination
    station is listed in that corridor.
    """

    corridor_departures = []

    for dep in departures:
        destination = dep.get("station")

        for corridor_name, stations in corridors.items():
            if destination in stations:
                dep["corridor"] = corridor_name
                corridor_departures.append(dep)

    return corridor_departures


