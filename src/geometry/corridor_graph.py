import networkx as nx
from shapely.geometry import LineString, MultiLineString

def railway_gdf_to_graph(gdf):
    """
    Convert railway LineString geometries into a NetworkX graph.
    Nodes are (x, y) coordinates.
    Edge weights are geometry length (meters).
    """
    G = nx.Graph()

    for geom in gdf.geometry:
        if isinstance(geom, LineString):
            lines = [geom]
        elif isinstance(geom, MultiLineString):
            lines = list(geom.geoms)
        else:
            continue

        for line in lines:
            coords = list(line.coords)

            for i in range(len(coords) - 1):
                p1 = coords[i]
                p2 = coords[i + 1]

                segment = LineString([p1, p2])
                length = segment.length

                G.add_edge(
                    p1,
                    p2,
                    weight=length,
                    geometry=segment
                )

    return G
