print("Pipeline booted")

# sanity tests done:

#from src.irail.corridors import CORRIDORS
#print(CORRIDORS)

# from src.geo.stations import STATIONS
# print("Ghent coords:", STATIONS["Ghent-Sint-Pieters"])

# from src.irail.liveboard import fetch_liveboard
# data = fetch_liveboard("Ghent-Sint-Pieters")
# print("Keys:", data.keys())
# print("Number of departures:", len(data["departures"]["departure"]))

from src.irail.liveboard import fetch_liveboard
from src.irail.corridor_filter import filter_corridor_trains

data = fetch_liveboard("Ghent-Sint-Pieters")
corridor_trains = filter_corridor_trains(data)

print(f"Found {len(corridor_trains)} corridor trains:")
for t in corridor_trains:
    print(t)
