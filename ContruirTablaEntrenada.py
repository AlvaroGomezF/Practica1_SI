from datetime import datetime
import sqlite3
import json


conn = sqlite3.connect('BBDD.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users_training(
            username TEXT PRIMARY KEY,
            telefono TEXT,
            contrasena TEXT,
            provincia TEXT,
            permisos INTEGER,
            total_emails INTEGER,
            phising_emails INTEGER,
            ciclado_emails INTEGER,
            critico INTEGER)
            ''')

with open('user_data_online_clasificado.json') as f:
    user_clasificados=json.load(f)


for usuario in user_clasificados['usuarios']:
    for username,info in usuario.items():
        c.execute("INSERT INTO users_training VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, info['telefono'], info['contrasena'], info['provincia'], info['permisos'], info['emails']['total'], info['emails']['phishing'], info['emails']['cliclados'],info['critico']))
conn.commit()
conn.close()