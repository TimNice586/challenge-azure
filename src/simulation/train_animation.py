import geopandas as gpd
import matplotlib.pyplot as plt
from src.geometry.corridor_builder import build_corridor_linestring
from src.geometry.parametric_curve import ParametricRailCurve
from src.simulation.train import Train
import contextily as ctx

# Example: load your corridor line from Phase 2
# Here, assume `path_geom` from shortest path is ready
line = path_geom  # LineString from previous steps

rail_curve = ParametricRailCurve(line)

# Multiple trains with different speeds and starting offsets
trains = [
    Train(rail_curve, speed=20, train_id="T1", start_distance=0),       # ~72 km/h
    Train(rail_curve, speed=15, train_id="T2", start_distance=5000),   # ~54 km/h, offset 5 km
    Train(rail_curve, speed=25, train_id="T3", start_distance=10000)   # ~90 km/h, offset 10 km
]

# Simple animation using matplotlib
plt.ion()  # interactive mode on
fig, ax = plt.subplots(figsize=(10, 10))

for t in range(0, 200):  # number of time steps
    ax.clear()
    
    # Plot corridor
    gpd.GeoSeries([line]).plot(ax=ax, color="blue", linewidth=2)
    
    # Move trains and plot positions
    positions = [train.move(dt=1) for train in trains]  # dt=1 second
    gpd.GeoSeries(positions).plot(ax=ax, color="red", markersize=20)
    
    # Optional: add train IDs as labels
    for train, pos in zip(trains, positions):
        ax.text(pos.x, pos.y, train.train_id, color="black", fontsize=10)
    
    ax.set_title(f"Train positions at t={t}s")
    ax.set_aspect("equal")
    plt.pause(0.05)  # pause to animate

plt.ioff()
plt.show()

# Reproject corridor and points to Web Mercator (EPSG:3857) for basemap
line_3857 = gpd.GeoSeries([line]).to_crs(epsg=3857)
positions_3857 = gpd.GeoSeries(positions).to_crs(epsg=3857)

# Plot with basemap
ax.clear()
line_3857.plot(ax=ax, color="blue", linewidth=2)
positions_3857.plot(ax=ax, color="red", markersize=20)
ctx.add_basemap(ax, source=ctx.providers.Stamen.TerrainBackground)

