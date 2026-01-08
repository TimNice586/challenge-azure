def corridor_bbox(corridor, padding=0.05):
    """
    Compute bounding box around a corridor with padding
    """
    latitudes = [corridor["from"]["lat"], corridor["to"]["lat"]]
    longitudes = [corridor["from"]["lon"], corridor["to"]["lon"]]

    return {
        "north": max(latitudes) + padding,
        "south": min(latitudes) - padding,
        "east": max(longitudes) + padding,
        "west": min(longitudes) - padding,
    }
