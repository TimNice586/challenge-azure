# test_parametric_corridor.py
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import (
    railway_gdf_to_graph,
    nearest_graph_node,
    shortest_path_geometry,
)
from src.geometry.corridor_builder import build_corridor_linestring
from src.geometry.parametric_curve import ParametricRailCurve
from src.reference.corridors import load_corridor_endpoints

# ----------------------------
# Load railway geometry
# ----------------------------
gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
gdf = gdf.to_crs(epsg=31370)

# ----------------------------
# Build graph & shortest path
# ----------------------------
G = railway_gdf_to_graph(gdf)
c = load_corridor_endpoints()["GHENT_BLANKENBERGE"]

p_from = gpd.GeoSeries([Point(c["from"]["lon"], c["from"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]
p_to = gpd.GeoSeries([Point(c["to"]["lon"], c["to"]["lat"])], crs="EPSG:4326").to_crs(epsg=31370).iloc[0]

n_from = nearest_graph_node(G, p_from)
n_to = nearest_graph_node(G, p_to)

nodes, path_geom = shortest_path_geometry(G, n_from, n_to)

# ----------------------------
# Build corridor LineString
# ----------------------------
line = path_geom  # already LineString from shortest_path_geometry

# ----------------------------
# Parametric curve
# ----------------------------
rail_curve = ParametricRailCurve(line)

# Test some points along the corridor
print("Start point:", rail_curve.position_at_distance(0))
print("Mid point:", rail_curve.position_at_distance(rail_curve.length / 2))
print("End point:", rail_curve.position_at_distance(rail_curve.length))

# Optional: plot the corridor and sample points
x, y = line.xy
plt.plot(x, y, color="blue", label="Corridor")

# Sample points
sample_distances = [0, rail_curve.length / 4, rail_curve.length / 2, 3*rail_curve.length/4, rail_curve.length]
for s in sample_distances:
    pt = rail_curve.position_at_distance(s)
    plt.plot(pt.x, pt.y, "ro")

plt.title("Parametric Corridor with Sample Points")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.legend()
plt.show()
