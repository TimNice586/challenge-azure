import os
import pyodbc
import sqlite3

DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # "sqlite" or "azure"
AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING", "")
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "../../data/departures.db")

def get_connection():
    """
    Returns a connection object depending on DB_TYPE
    """
    if DB_TYPE == "azure":
        if not AZURE_SQL_CONNECTION_STRING:
            raise ValueError("AZURE_SQL_CONNECTION_STRING not set in environment")
        conn = pyodbc.connect(AZURE_SQL_CONNECTION_STRING)
        return conn
    elif DB_TYPE == "sqlite":
        conn = sqlite3.connect(SQLITE_PATH)
        return conn
    else:
        raise ValueError(f"Unknown DB_TYPE: {DB_TYPE}")
