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



#Apartado 4
query4='''SELECT creacion AS añosBueno FROM legal
WHERE cookies = 1 AND aviso = 1 AND proteccion_de_datos = 1
'''

queryMalos='''SELECT creacion AS añosMalo FROM legal
WHERE cookies = 0 OR aviso = 0 OR proteccion_de_datos = 0'''


dfAñosBueno=pd.read_sql_query(query4,conn)
dfAñosMalo=pd.read_sql_query(queryMalos,conn)
print(dfAñosBueno)
print(len(dfAñosBueno))
print(dfAñosMalo)
print(len(dfAñosMalo))

mediaAñosBueno=dfAñosBueno['añosBueno'].mean()
mediaAñosMalo=dfAñosMalo['añosMalo'].mean()

print(mediaAñosBueno,mediaAñosMalo)

listaAños=[mediaAñosBueno, mediaAñosMalo]
listaCategorias=["Webs cumplen políticas","Webs no cumplen políticas"]


# Crear el gráfico de barras
plt.bar(listaCategorias, listaAños, color=['green', 'red'])
plt.xlabel('Categoría de Webs')
plt.ylabel('Años de creación (media)')
plt.title('Media de años de creación según cumplimiento de políticas')
plt.ylim(2010, 2015)
plt.show()
#print(dfAñosBueno['webs_totales'])



query = '''
SELECT creacion AS año,
       SUM(CASE WHEN cookies = 1 AND aviso = 1 AND proteccion_de_datos = 1 THEN 1 ELSE 0 END) AS añosBueno,
       SUM(CASE WHEN cookies = 0 OR aviso = 0 OR proteccion_de_datos = 0 THEN 1 ELSE 0 END) AS añosMalo
FROM legal
GROUP BY creacion
'''

# Ejecutar la consulta y guardar los resultados en un DataFrame
df = pd.read_sql_query(query, conn)

# Generar una lista de todos los años desde 2000 hasta 2020
todos_los_años = pd.DataFrame({'año': range(2000, 2024)})

# Fusionar el DataFrame de todos los años con los datos obtenidos de la consulta
df = todos_los_años.merge(df, on='año', how='left').fillna(0)

# Crear el gráfico de barras
ancho_barra = 0.4  # Ancho de cada barra
plt.bar(df['año'] - ancho_barra/2, df['añosBueno'], width=ancho_barra, color='green', label='Buenos')
plt.bar(df['año'] + ancho_barra/2, df['añosMalo'], width=ancho_barra, color='red', label='Malos')

plt.xlabel('Año de Creación')
plt.ylabel('Cantidad de Webs')
plt.title('Cantidad de Webs Buenas y Malas por Año de Creación')
plt.legend()

plt.xticks(range(2000, 2024), rotation=45)  # Establecer las etiquetas del eje x para mostrar todos los años

plt.tight_layout()
plt.show()