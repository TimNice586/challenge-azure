import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import railway_gdf_to_graph, nearest_graph_node, shortest_path_geometry
from src.reference.corridors import load_corridor_endpoints
from src.geometry.corridor_builder import build_corridor_linestring
from src.geometry.parametric_curve import ParametricRailCurve
from src.simulation.train import Train

# ------------------------------
# Step 1: Load corridor geometry
# ------------------------------
corridor_name = "GHENT_BLANKENBERGE"
gdf = load_railway_geometry_for_corridor(corridor_name)
gdf = gdf.to_crs(epsg=31370)

# Build graph
G = railway_gdf_to_graph(gdf)

# Corridor endpoints
c = load_corridor_endpoints()[corridor_name]

p_from = gpd.GeoSeries([Point(c["from"]["lon"], c["from"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]
p_to   = gpd.GeoSeries([Point(c["to"]["lon"], c["to"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]

# ------------------------------
# Step 2: Shortest path
# ------------------------------
nodes, path_geom = shortest_path_geometry(G, nearest_graph_node(G, p_from), nearest_graph_node(G, p_to))
print("Path nodes:", len(nodes))
print("Path length (meters):", path_geom.length)

line = build_corridor_linestring(path_geom) if hasattr(path_geom, "geometry") else path_geom

# Create parametric curve
rail_curve = ParametricRailCurve(line)

# ------------------------------
# Step 3: Initialize trains
# ------------------------------
trains = [
    Train(rail_curve, speed=20, train_id="T1", start_distance=0),
    Train(rail_curve, speed=15, train_id="T2", start_distance=5000),
    Train(rail_curve, speed=25, train_id="T3", start_distance=10000),
]

# ------------------------------
# Step 4: Animate trains
# ------------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))

for t in range(200):
    ax.clear()
    # Plot corridor
    gpd.GeoSeries([line]).plot(ax=ax, color="blue", linewidth=2)
    # Move trains
    positions = [train.move(dt=1) for train in trains]
    gpd.GeoSeries(positions).plot(ax=ax, color="red", markersize=20)
    # Labels
    for train, pos in zip(trains, positions):
        ax.text(pos.x, pos.y, train.train_id, color="black", fontsize=10)
    ax.set_aspect("equal")
    plt.pause(0.05)

plt.ioff()
plt.show()
