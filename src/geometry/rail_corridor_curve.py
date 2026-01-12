import geopandas as gpd
from shapely.geometry import Point

from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_graph import (
    railway_gdf_to_graph,
    nearest_graph_node,
    shortest_path_geometry
)
from src.geometry.corridor_builder import build_corridor_linestring
from src.geometry.parametric_curve import ParametricRailCurve
from src.reference.corridors import load_corridor_endpoints


def build_ghent_blankenberge_curve():
    """
    Build a ParametricRailCurve following the real railway track
    Ghent-Sint-Pieters → Blankenberge
    """
    # 1. Load railway geometry
    gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
    gdf = gdf.to_crs(epsg=31370)  # Belgian Lambert 72 (meters)

    # 2. Build graph
    G = railway_gdf_to_graph(gdf)

    # 3. Load corridor endpoints
    corridor = load_corridor_endpoints()["GHENT_BLANKENBERGE"]

    p_from = gpd.GeoSeries(
        [Point(corridor["from"]["lon"], corridor["from"]["lat"])],
        crs="EPSG:4326"
    ).to_crs(epsg=31370).iloc[0]

    p_to = gpd.GeoSeries(
        [Point(corridor["to"]["lon"], corridor["to"]["lat"])],
        crs="EPSG:4326"
    ).to_crs(epsg=31370).iloc[0]

    # 4. Snap to rail graph
    n_from = nearest_graph_node(G, p_from)
    n_to = nearest_graph_node(G, p_to)

    # 5. Shortest rail path
    _, path_geom = shortest_path_geometry(G, n_from, n_to)

    # 6. Merge into single LineString
    line = build_corridor_linestring(
        gpd.GeoDataFrame(geometry=[path_geom], crs="EPSG:31370")
    )

    # 7. Return parametric curve
    return ParametricRailCurve(line)