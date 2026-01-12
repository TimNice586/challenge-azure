import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.geometry.train_position import get_active_trains, compute_train_position

# -----------------------------
# 1. Use environment variable
# -----------------------------
DB_CONNECTION_STRING = os.environ.get("SQL_CONNECTION_STRING")

if not DB_CONNECTION_STRING:
    raise ValueError("SQL_CONNECTION_STRING environment variable is not set!")

# -----------------------------
# 2. FastAPI app
# -----------------------------
app = FastAPI(title="Belgian Trains API")

# Allow frontend to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------
# 3. Endpoint to get active trains
# -----------------------------
@app.get("/active_trains")
def active_trains():
    # Connect to Azure SQL
    # Note: sqlite3 won't work for Azure SQL, you must use pyodbc
    import pyodbc

    conn = pyodbc.connect(DB_CONNECTION_STRING)
    
    train_ids = get_active_trains(conn)

    positions = []
    for tid in train_ids:
        pos = compute_train_position(tid)
        if pos:
            positions.append(pos)

    conn.close()
    return positions
