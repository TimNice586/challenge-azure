from shapely.ops import unary_union
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge
import geopandas as gpd

def merge_railway_geometries(gdf: gpd.GeoDataFrame):
    """
    Merge multiple railway LineStrings into a single geometry.
    Returns a MultiLineString or LineString.
    """
    geometries = list(gdf.geometry)
    merged = unary_union(geometries)
    return merged

def build_corridor_linestring(path_edges_gdf):
    """
    Merge ordered path edge geometries into a single LineString.
    """
    merged = linemerge(path_edges_gdf.geometry.values)

    if merged.geom_type != "LineString":
        raise ValueError(f"Expected LineString, got {merged.geom_type}")

    return merged