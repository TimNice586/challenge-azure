CREATE TABLE IF NOT EXISTS corridor_departures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    station_departure TEXT NOT NULL,
    vehicle TEXT NOT NULL,
    train_type TEXT NOT NULL,
    delay_seconds INTEGER,
    platform TEXT,
    corridor TEXT NOT NULL,
    UNIQUE(timestamp, vehicle, corridor)
);
