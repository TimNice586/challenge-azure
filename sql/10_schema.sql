-- =========================
-- TRAINS
-- =========================
CREATE TABLE IF NOT EXISTS trains (
    train_id TEXT PRIMARY KEY,
    train_type TEXT,
    origin_station TEXT,
    destination_station TEXT
);

-- =========================
-- STATIONS
-- =========================
CREATE TABLE IF NOT EXISTS stations (
    station_id TEXT PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL
);

-- =========================
-- TRAIN STOPS
-- =========================
CREATE TABLE IF NOT EXISTS train_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_id TEXT,
    station_id TEXT,
    scheduled_arrival INTEGER,
    scheduled_departure INTEGER,
    actual_arrival INTEGER,
    actual_departure INTEGER,
    delay INTEGER,

    FOREIGN KEY(train_id) REFERENCES trains(train_id),
    FOREIGN KEY(station_id) REFERENCES stations(station_id)
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_train_stops_train
ON train_stops(train_id);

CREATE INDEX IF NOT EXISTS idx_train_stops_station
ON train_stops(station_id);
