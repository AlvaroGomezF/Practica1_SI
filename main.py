import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect('BBDD.db')
c = conn.cursor()

# Leer datos de legal.json
with open('legal_data_online.json') as f:
    legal_data = json.load(f)

# Crear tabla para legal.json
c.execute('''CREATE TABLE legal (
                web TEXT PRIMARY KEY,
                cookies INTEGER,
                aviso INTEGER,
                proteccion_de_datos INTEGER,
                creacion INTEGER
            )''')

# Insertar datos en la tabla
for item in legal_data['legal']:
    for web, info in item.items():
        c.execute("INSERT INTO legal VALUES (?, ?, ?, ?, ?)", (web, info['cookies'], info['aviso'], info['proteccion_de_datos'], info['creacion']))

# Leer datos de users.json
with open('users_data_online.json') as f:
    users_data = json.load(f)

# Crear tabla para users.json
c.execute('''CREATE TABLE users (
                username TEXT PRIMARY KEY,
                telefono TEXT,
                contrasena TEXT,
                provincia TEXT,
                permisos INTEGER,
                total_emails INTEGER,
                phishing_emails INTEGER,
                cliclados_emails INTEGER
            )''')

# Insertar datos en la tabla
for user in users_data['usuarios']:
    for username, info in user.items():
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (username, info['telefono'], info['contrasena'], info['provincia'], info['permisos'], info['emails']['total'], info['emails']['phishing'], info['emails']['cliclados']))

# Guardar los cambios
conn.commit()
conn.close()

