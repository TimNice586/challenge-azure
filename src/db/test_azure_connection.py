import pyodbc

server = "trainpipeline-server.database.windows.net"
database = "iRailDB"
username = "CloudSAdd56d68e"
password = "Ham4Zi!Fa?ti"

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Uid={username};"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT @@VERSION;")
row = cursor.fetchone()

print("Connected successfully!")
print(row[0])

conn.close()
