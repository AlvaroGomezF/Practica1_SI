import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('BBDD.db')

# Obtener datos de conexiones de usuarios por día
query = """
    SELECT ip, fecha
    FROM user_ips
"""
df = pd.read_sql_query(query, conn)

# Convertir la columna 'fecha' a tipo de dato de fecha
df['fecha'] = pd.to_datetime(df['fecha'])

# Crear una nueva columna 'dia' que contenga solo la fecha (sin la hora) para agrupar por día
df['dia'] = df['fecha'].dt.date

# Contar conexiones por día de usuario
conexiones_por_dia = df.groupby(['dia', 'ip']).size().reset_index(name='conexiones')

print("Conexiones por día de usuario:")
print(conexiones_por_dia)
