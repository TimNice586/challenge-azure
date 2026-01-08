# test_corridor_map.py
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import railway_gdf_to_graph, nearest_graph_node, shortest_path_geometry
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
# Interpolate points
# ----------------------------
ds = 20  # meters
points = [rail_curve.position_at_distance(s) for s in range(0, int(rail_curve.length)+1, ds)]
gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:31370")

# ----------------------------
# Reproject to WGS84 (lat/lon) for mapping
# ----------------------------
gdf_corridor = gpd.GeoDataFrame(geometry=[rail_curve.line], crs="EPSG:31370").to_crs(epsg=4326)
gdf_points = gdf_points.to_crs(epsg=4326)

# ----------------------------
# Plot on Belgian map
# ----------------------------
fig, ax = plt.subplots(figsize=(12, 12), dpi=150)

buffer = 0.02  # degrees (~2 km roughly)
minx, miny, maxx, maxy = gdf_corridor.total_bounds
ax.set_xlim(minx - buffer, maxx + buffer)
ax.set_ylim(miny - buffer, maxy + buffer)

gdf_corridor.plot(ax=ax, color="blue", linewidth=2, label="Corridor")
gdf_points.plot(ax=ax, color="red", markersize=5, label="Interpolated Points")


ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf_corridor.crs.to_string())
plt.title("Corridor on Belgian Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()
