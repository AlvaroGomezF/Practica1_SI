import hashlib

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3

def calcular_hashes(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        hashed_passwords = set(hashlib.md5(passwd.encode()).hexdigest() for passwd in passwords)
    return hashed_passwords
def compararHashes(hashes_bd,hashes_dicc):
    resultado = []

    for i in hashes_bd:
        if i in hashes_dicc:
            resultado.append("Debil")
        else:
            resultado.append("Fuerte")
    return resultado

conn = sqlite3.connect('BBDD.db')
# Consulta para obtener las fechas de cambio de contraseña por usuario
query = """
    SELECT u.username, u.permisos, ui.fecha
    FROM users u
    INNER JOIN user_ips ui ON u.username = ui.username
    WHERE u.contrasena IS NOT NULL
"""

# Leer los datos de la consulta en un DataFrame
df = pd.read_sql_query(query, conn)

df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # 'coerce' para manejar valores no válidos convirtiéndolos en NaT (Not a Time)

# Ordenar el DataFrame por 'username' y 'fecha' dentro de cada usuario
df_sorted = df.sort_values(by=['username', 'fecha'])

# Calcular la diferencia de tiempo entre cambios de fecha para cada usuario
df_sorted['diferencia'] = df_sorted.groupby('username')['fecha'].diff().dt.days

# Separar usuarios normales de administradores
usuarios_normales = df_sorted[df_sorted['permisos'] == 0]
usuarios_administradores = df_sorted[df_sorted['permisos'] == 1]

# Calcular la media de tiempo entre cambios de contraseña para usuarios normales y administradores
media_tiempo_normales = usuarios_normales['diferencia'].mean()
media_tiempo_administradores = usuarios_administradores['diferencia'].mean()

print("Media de tiempo entre cambios de contraseña para usuarios normales:", media_tiempo_normales)
print("Media de tiempo entre cambios de contraseña para usuarios administradores:", media_tiempo_administradores)

#Ahora creamos el grafico :

listasMedias=[media_tiempo_normales,media_tiempo_administradores]
listaCat=['Usuarios Normales','Usuarios Admin']

plt.bar(listaCat,listasMedias,color=['yellow','red'])
plt.title('Media de tiempo de cambio de contraseña por Tipo de Usuario')
plt.xlabel('Tipo de Usuario')
plt.ylabel('Media de Tiempo')
plt.show()

#Apartado 2:
query1='''SELECT username,contrasena from users'''
query2='''SELECT username,phishing_emails,cliclados_emails from users'''
dfUsuarios = pd.read_sql_query(query1, conn)
dfCorreos=pd.read_sql_query(query2,conn)

dfCorreos['probabilidad']=dfCorreos['cliclados_emails']/dfCorreos['phishing_emails']
hashes_sry=calcular_hashes('SRY.txt')
dfUsuarios['robustez']=compararHashes(dfUsuarios['contrasena'],hashes_sry)
usuariosDebiles=dfUsuarios[dfUsuarios['robustez']=='Debil']

usuariosMasCriticos=usuariosDebiles.merge(dfCorreos,on='username')

usuarios10=usuariosMasCriticos.nlargest(10,'probabilidad')

plt.barh(usuarios10['username'], usuarios10['probabilidad'], color='skyblue')
plt.xlabel('Probabilidad')
plt.ylabel('Usuarios')
plt.title('Usuarios con mayor criticidad')
plt.show()
#Apartado 3


