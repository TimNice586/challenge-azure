from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from src.geometry.train_position import get_active_trains, compute_train_position, DB_PATH
from shapely.geometry import mapping
from src.geometry.rail_corridor_curve import build_ghent_blankenberge_curve
from fastapi.responses import JSONResponse
import geopandas as gpd

app = FastAPI(title="Belgian Trains API")

# Optional: allow JS frontend to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your domain
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/active_trains")
def active_trains():
    conn = sqlite3.connect(DB_PATH)
    train_ids = get_active_trains(conn)
    conn.close()

    positions = []
    for tid in train_ids:
        pos = compute_train_position(tid)
        if pos:
            positions.append(pos)

    return positions

@app.get("/rail_corridor")
def rail_corridor():
    curve = build_ghent_blankenberge_curve()

    geojson = {
        "type": "Feature",
        "geometry": mapping(curve.line),
        "properties": {
            "length_m": curve.length
        }
    }

    return geojson

@app.get("/railway_corridor")
def railway_corridor():
    """
    Return the exact rail corridor geometry used for interpolation
    """
    curve = build_ghent_blankenberge_curve()

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        geometry=[curve.line],
        crs="EPSG:31370"
    ).to_crs(epsg=4326)

    return JSONResponse(gdf.__geo_interface__)