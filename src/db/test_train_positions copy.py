
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import railway_gdf_to_graph, nearest_graph_node, shortest_path_geometry
from src.reference.corridors import load_corridor_endpoints
from src.geometry.corridor_builder import build_corridor_linestring
from src.geometry.parametric_curve import ParametricRailCurve
from src.geometry.rail_corridor_curve import build_ghent_blankenberge_curve

# ------------------------
# 1. Load railway geometry
# ------------------------
gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
gdf = gdf.to_crs(epsg=31370)  # Belgian Lambert 72

# ------------------------
# 2. Build graph
# ------------------------
G = railway_gdf_to_graph(gdf)

# ------------------------
# 3. Load corridor endpoints
# ------------------------
c = load_corridor_endpoints()["GHENT_BLANKENBERGE"]

p_from = gpd.GeoSeries([Point(c["from"]["lon"], c["from"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]
p_to   = gpd.GeoSeries([Point(c["to"]["lon"], c["to"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]

n_from = nearest_graph_node(G, p_from)
n_to   = nearest_graph_node(G, p_to)

# ------------------------
# 4. Shortest path
# ------------------------
nodes, path_geom = shortest_path_geometry(G, n_from, n_to)

print("Path nodes:", len(nodes))
print("Path length (meters):", path_geom.length)

# ------------------------
# 5. Build LineString for the corridor
# ------------------------
# path_geom is already a LineString (not a GeoDataFrame), so we pass it as a list
line = build_corridor_linestring(gpd.GeoDataFrame(geometry=[path_geom]))

print(type(line))
print("Corridor length (m):", line.length)

# ------------------------
# 6. Create parametric rail curve
# ------------------------
rail_curve = ParametricRailCurve(line)

# ------------------------
# 7. Interpolate train positions
# ------------------------
# Increase resolution: e.g., every 5 meters
step_size = 5  # meters
distances = range(0, int(rail_curve.length), step_size)

train_points = [rail_curve.position_at_distance(s) for s in distances]

# Convert to GeoDataFrame for plotting
gdf_points = gpd.GeoDataFrame(
    geometry=gpd.points_from_xy([p.x for p in train_points], [p.y for p in train_points]),
    crs="EPSG:31370"
)

print("Number of interpolated points:", len(gdf_points))
print(gdf_points.head())

# ------------------------
# 8. Plot corridor + train positions
# ------------------------
fig, ax = plt.subplots(figsize=(12, 8))

# Corridor in blue
gpd.GeoSeries(line).plot(ax=ax, color="blue", linewidth=2, label="Rail corridor")

# Train points in red
gdf_points.plot(ax=ax, color="red", markersize=5, label="Train positions")

ax.set_title("Train positions along corridor (high resolution)")
ax.legend()
plt.show()

