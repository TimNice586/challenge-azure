from src.geometry.railway_loader import load_railway_geometry_for_corridor
from src.geometry.corridor_builder import merge_railway_geometries

gdf = load_railway_geometry_for_corridor("GHENT_BLANKENBERGE")
merged = merge_railway_geometries(gdf)

# Step 2.2.4 — reproject to metric CRS
gdf_proj = gdf.to_crs(epsg=31370)  # Belgian Lambert 72

merged_proj = gdf_proj.union_all()

print(type(merged_proj))
print(merged_proj.geom_type)
print("Total length (meters):", merged_proj.length)

#print(type(merged))
#print(merged)