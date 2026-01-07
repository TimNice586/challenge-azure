from src.irail.liveboard import fetch_liveboard
from src.irail.corridors import CORRIDORS
from src.pipeline.corridor_filter import filter_corridor_departures
from src.pipeline.normalizer import normalize_departure

print("Pipeline booted")

data = fetch_liveboard("Ghent-Sint-Pieters")
departures = data["departures"]["departure"]

corridor_trains = filter_corridor_departures(departures, CORRIDORS)

events = [normalize_departure(dep) for dep in corridor_trains]

print(f"Found {len(events)} corridor trains")

for event in events[:5]:
    print(event)
