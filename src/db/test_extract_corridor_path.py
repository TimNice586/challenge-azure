from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import railway_gdf_to_graph

gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
G = railway_gdf_to_graph(gdf)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
