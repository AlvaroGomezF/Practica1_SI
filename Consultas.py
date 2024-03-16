import sqlite3
import pandas as pd

# Conexión a la base de datos SQLite
conn = sqlite3.connect('empresa.db')

# Consultas SQL
queries = [
    "SELECT COUNT(*) FROM users",
    "SELECT AVG(LENGTH(fechas)), AVG(LENGTH(ips)), AVG(total_emails), AVG(phishing_emails) FROM users",
    "SELECT MIN(total_emails), MAX(total_emails), MIN(phishing_emails), MAX(phishing_emails) FROM users WHERE permisos = 1"
]

# Ejecutar consultas y cargar los resultados en un DataFrame
results = []
for query in queries:
    result = pd.read_sql_query(query, conn)
    results.append(result)

# Mostrar los resultados
for result in results:
    print(result)

# Cerrar la conexión
conn.close()
