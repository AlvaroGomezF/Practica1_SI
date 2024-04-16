from datetime import datetime

import pandas as pd
import numpy as np
import sqlite3
import hashlib


conn = sqlite3.connect('BBDD.db')
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarioslogin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        fecha DATE
    )
''')
conn.commit()

def registrar_usuario(username, password, fecha=None):
    # Si no se proporciona una fecha, se utiliza la fecha y hora actual
    if fecha is None:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Hash de la contraseña
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute('''
            INSERT INTO usuarioslogin (username, password, fecha) VALUES (?, ?, ?)
        ''', (username, hashed_password, fecha))
        conn.commit()
        print("Usuario registrado exitosamente.")
    except sqlite3.IntegrityError:
        print("El nombre de usuario ya está en uso.")

def verificar_credenciales(username, password):
    # Hash de la contraseña proporcionada
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('''
        SELECT * FROM usuarioslogin WHERE username=? AND password=?
    ''', (username, hashed_password))
    user = cursor.fetchone()
    if user:
        print("Inicio de sesión exitoso.")
    else:
        print("Credenciales incorrectas.")

# Ejemplo de registro de usuario
registrar_usuario('usuario2', 'password123', '2024-04-17 11:58:00')

# Ejemplo de inicio de sesión
verificar_credenciales('usuario1', 'password123')

# Obtener datos de conexiones de usuarios por día
query = """
    SELECT username, fecha
    FROM usuarioslogin
"""
df = pd.read_sql_query(query, conn)

# Convertir la columna 'fecha' a tipo de dato de fecha
df['fecha'] = pd.to_datetime(df['fecha'])

# Crear una nueva columna 'dia' que contenga solo la fecha (sin la hora) para agrupar por día
df['dia'] = df['fecha'].dt.date

# Contar conexiones por día de usuario
conexiones_por_dia = df.groupby(['dia', 'username'])['username'].nunique().reset_index(name='conexiones')
print("Conexiones por día de usuario:")
print(conexiones_por_dia)