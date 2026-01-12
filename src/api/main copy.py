from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from src.geometry.train_position import get_active_trains, compute_train_position, DB_PATH
from shapely.geometry import mapping
from src.geometry.rail_corridor_curve import build_ghent_blankenberge_curve

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