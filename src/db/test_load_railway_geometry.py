from src.geometry.railway_loader import load_railway_geometry_for_corridor

gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
print(gdf.head())
print(f"Loaded {len(gdf)} railway geometries")
