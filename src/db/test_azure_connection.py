import pyodbc
from src.config.azure_sql import get_azure_conn_str

conn_str = get_azure_conn_str()

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT @@VERSION;")
row = cursor.fetchone()

print("Connected successfully!")
print(row[0])

conn.close()
