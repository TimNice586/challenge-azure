import os
import osmnx as ox
import geopandas as gpd
from shapely.geometry import LineString, MultiLineString, box
from src.reference.corridors import load_corridor_endpoints

CACHE_DIR = "data/geo_cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def corridor_bbox(corridor, padding=0.02):
    """
    Compute a bounding box for a corridor with some padding (degrees)
    Returns shapely box
    """
    latitudes = [corridor["from"]["lat"], corridor["to"]["lat"]]
    longitudes = [corridor["from"]["lon"], corridor["to"]["lon"]]

    north = max(latitudes) + padding
    south = min(latitudes) - padding
    east = max(longitudes) + padding
    west = min(longitudes) - padding

    return box(west, south, east, north)  # shapely box


def load_railway_geometry_for_corridor(corridor_name, force_reload=False):
    """
    Load railway geometry (OSM polylines) for a corridor.
    Will cache the result in a GeoJSON to avoid repeated Overpass queries.
    Returns a GeoDataFrame of LineStrings
    """
    corridors = load_corridor_endpoints()
    if corridor_name not in corridors:
        raise ValueError(f"Corridor {corridor_name} not found")

    corridor = corridors[corridor_name]
    bbox_geom = corridor_bbox(corridor)

    cache_file = os.path.join(CACHE_DIR, f"{corridor_name.lower()}.geojson")
    if os.path.exists(cache_file) and not force_reload:
        print(f"Loading cached railway geometry for {corridor_name}")
        gdf = gpd.read_file(cache_file)
        return gdf

    print(f"Fetching railway geometry from OSM for {corridor_name}...")
    tags = {"railway": "rail"}

    # ✅ Correct way with latest OSMnx: pass polygon geometry
    gdf = ox.features_from_polygon(bbox_geom, tags=tags)

    # Filter only LineString / MultiLineString geometries
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]

    # Save to cache
    gdf.to_file(cache_file, driver="GeoJSON")
    print(f"Saved railway geometry to {cache_file}")

    return gdf


def simplify_geometries(gdf):
    """
    Optional: merge all lines into one MultiLineString to simplify interpolation
    """
    gdf = gdf.copy()
    gdf["geometry"] = gdf["geometry"].apply(
        lambda geom: geom if isinstance(geom, LineString) else LineString(geom.coords)
    )
    return gdf


