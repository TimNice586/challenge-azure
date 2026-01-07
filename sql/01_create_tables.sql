CREATE TABLE train_departures (
    timestamp DATETIME2 NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL,
    destination_station VARCHAR(100) NOT NULL,
    corridor VARCHAR(50) NOT NULL,
    train_type VARCHAR(10),
    delay_seconds INT,
    platform VARCHAR(10),

    CONSTRAINT pk_train_departures
        PRIMARY KEY (vehicle_id, timestamp, corridor)
);
