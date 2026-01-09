from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List, Dict
from src.db.connection import get_connection

app = FastAPI(title="Live Train API")

# -----------------------------
# Utility function to fetch active trains
# -----------------------------
def fetch_active_trains() -> List[Dict]:
    """
    Fetch active trains from the database.
    Returns a list of dictionaries for each train.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                train_id,
                vehicle,
                dep_station,
                arr_station,
                dep_time,
                arr_time,
                delay_seconds,
                occupancy,
                last_updated
            FROM active_trains
            ORDER BY dep_time
        """)
        rows = cursor.fetchall()

        trains = []
        for row in rows:
            trains.append({
                "train_id": row[0],
                "vehicle": row[1],
                "dep_station": row[2],
                "arr_station": row[3],
                "dep_time": row[4].isoformat() if isinstance(row[4], datetime) else row[4],
                "arr_time": row[5].isoformat() if isinstance(row[5], datetime) else row[5],
                "delay_seconds": row[6],
                "occupancy": row[7],
                "last_updated": row[8].isoformat() if isinstance(row[8], datetime) else row[8]
            })

        return trains

    finally:
        cursor.close()
        conn.close()

# -----------------------------
# API Endpoint
# -----------------------------
@app.get("/active_trains", response_model=List[Dict])
def get_active_trains():
    """
    Returns the current active trains.
    """
    try:
        trains = fetch_active_trains()
        return trains
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

