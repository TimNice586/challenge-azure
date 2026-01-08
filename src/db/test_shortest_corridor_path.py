from shapely.geometry import Point
import geopandas as gpd

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import (
    railway_gdf_to_graph,
    nearest_graph_node,
    shortest_path_geometry,
)
from src.reference.corridors import load_corridor_endpoints

# Load railway geometry
gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
gdf = gdf.to_crs(epsg=31370)

# Build graph
G = railway_gdf_to_graph(gdf)

# Corridor endpoints
c = load_corridor_endpoints()["GHENT_BLANKENBERGE"]

p_from = gpd.GeoSeries(
    [Point(c["from"]["lon"], c["from"]["lat"])],
    crs="EPSG:4326"
).to_crs(epsg=31370).iloc[0]

p_to = gpd.GeoSeries(
    [Point(c["to"]["lon"], c["to"]["lat"])],
    crs="EPSG:4326"
).to_crs(epsg=31370).iloc[0]

n_from = nearest_graph_node(G, p_from)
n_to = nearest_graph_node(G, p_to)

nodes, path_geom = shortest_path_geometry(G, n_from, n_to)

print("Path nodes:", len(nodes))
print("Path length (meters):", path_geom.length)
