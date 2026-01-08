# test_interpolated_corridor.py
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import (
    railway_gdf_to_graph,
    nearest_graph_node,
    shortest_path_geometry,
)
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
rail_curve = ParametricRailCurve(path_geom)

# ----------------------------
# Interpolate points along the corridor
# ----------------------------
ds = 50  # meters
points = [rail_curve.position_at_distance(s) for s in range(0, int(rail_curve.length)+1, ds)]
gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:31370")

print("Number of interpolated points:", len(gdf_points))
print(gdf_points.head())

# ----------------------------
# Plot corridor and interpolated points
# ----------------------------
x_corr, y_corr = rail_curve.line.xy
plt.plot(x_corr, y_corr, color="blue", label="Corridor")

x_pts = [p.x for p in points]
y_pts = [p.y for p in points]
plt.scatter(x_pts, y_pts, color="red", s=10, label="Interpolated Points")

plt.title("Interpolated Corridor Points")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.legend()
plt.show()
