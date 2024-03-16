from datetime import datetime
import sqlite3
import json

# Conexión a la base de datos SQLite
conn = sqlite3.connect('BBDD.db')
c = conn.cursor()

# Leer datos de legal.json
with open('legal_data_online.json') as f:
    legal_data = json.load(f)

# Crear tabla para legal.json
c.execute('''CREATE TABLE IF NOT EXISTS legal (
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
c.execute('''CREATE TABLE IF NOT EXISTS users (
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


# Crear tabla para IP y fechas
c.execute('''CREATE TABLE IF NOT EXISTS user_ips (
                username TEXT,
                ip TEXT,
                fecha DATE,
                FOREIGN KEY (username) REFERENCES users(username)
            )''')


# Insertar datos en la tabla de IP y fechas
for user in users_data['usuarios']:
    username = list(user.keys())[0]  # Obtiene el nombre de usuario
    ip_data = user[username]['ips']   # Obtiene los datos de IP
    date_data = user[username]['fechas']  #Obtiene los datos de las fechas

    # Iterar sobre las IPs y fechas al mismo tiempo
    for ip, fecha_str in zip(ip_data, date_data):
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        c.execute("INSERT INTO user_ips VALUES (?, ?, ?)", (username, ip, fecha))

# Guardar los cambios
conn.commit()
conn.close()

