import networkx as nx
from shapely.geometry import LineString, MultiLineString
from shapely.geometry import Point
import math

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

def nearest_graph_node(G, point):
    """
    Find the nearest graph node to a shapely Point.
    Graph nodes are (x, y) tuples.
    """
    min_dist = float("inf")
    nearest = None

    px, py = point.x, point.y

    for nx_, ny_ in G.nodes:
        dx = nx_ - px
        dy = ny_ - py
        dist = dx * dx + dy * dy  # squared distance

        if dist < min_dist:
            min_dist = dist
            nearest = (nx_, ny_)

    return nearest

def shortest_path_geometry(G, start_node, end_node):
    """
    Compute shortest path (by edge length) and return:
    - list of nodes
    - LineString geometry of the path
    """
    path_nodes = nx.shortest_path(
        G,
        source=start_node,
        target=end_node,
        weight="length"
    )

    from shapely.geometry import LineString
    path_line = LineString(path_nodes)

    return path_nodes, path_line