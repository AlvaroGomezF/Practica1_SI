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

def iniciar_sesion(username, password):
    # Verificar credenciales
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('''
        SELECT * FROM usuarioslogin WHERE username=? AND password=?
    ''', (username, hashed_password))
    user = cursor.fetchone()
    if user:
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Credenciales incorrectas.")
        return False

def contar_sesiones_por_dia(username, fecha):
    cursor.execute('''
        SELECT COUNT(*) FROM usuarioslogin WHERE username=? AND strftime('%Y-%m-%d', fecha)=?
    ''', (username, fecha))
    sesiones = cursor.fetchone()[0]
    print(f"El usuario {username} ha iniciado sesión {sesiones} veces el {fecha}.")

# Ejemplo de registro de usuario solo si no está registrado previamente
try:
    registrar_usuario('usuario1', 'password123', '2024-06-19 11:59:00')
except:
    pass

# Ejemplo de inicio de sesión
iniciar_sesion('usuario1', 'password123')

# Contar las sesiones del usuario 'usuario1' el 2024-06-19
contar_sesiones_por_dia('usuario1', '2024-06-19')
