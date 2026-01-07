def insert_departures_azure(departures, conn_str):
    import pyodbc

    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        for dep in departures:
            cursor.execute("""
                INSERT INTO departures (timestamp, station_departure, vehicle, train_type, delay_seconds, platform, corridor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, dep['timestamp'], dep['station_departure'], dep['vehicle'],
                 dep['train_type'], dep['delay_seconds'], dep['platform'], dep['corridor'])
        conn.commit()
