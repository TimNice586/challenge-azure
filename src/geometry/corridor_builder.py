from shapely.ops import unary_union
from shapely.geometry import LineString, MultiLineString
import geopandas as gpd

def merge_railway_geometries(gdf: gpd.GeoDataFrame):
    """
    Merge multiple railway LineStrings into a single geometry.
    Returns a MultiLineString or LineString.
    """
    geometries = list(gdf.geometry)
    merged = unary_union(geometries)
    return merged