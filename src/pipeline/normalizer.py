from datetime import datetime


def normalize_departure(dep: dict) -> dict:
    """
    Convert a raw iRail departure object into
    a clean, flat event record.
    """

    return {
        "timestamp": datetime.fromtimestamp(int(dep["time"])),
        "station_departure": dep.get("station"),
        "vehicle": dep.get("vehicle"),
        "train_type": dep.get("vehicleinfo", {}).get("type"),
        "delay_seconds": int(dep.get("delay", 0)),
        "platform": dep.get("platform"),
        "corridor": dep.get("corridor"),
    }
