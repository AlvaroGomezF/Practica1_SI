import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# Conectarse a la base de datos
conn = sqlite3.connect('BBDD.db')

#Apartado 1:
query="SELECT COUNT(*) AS num_muestras FROM users"
df = pd.read_sql_query(query, conn)
num_muestras = df['num_muestras'].iloc[0]  # Obtener el valor de 'num_muestras' de la primera fila
print("Apartado 1")
print("Número total de muestras:", num_muestras)

#Apartado 2:
query = "SELECT ip, fecha FROM user_ips"
# Leer los datos en un DataFrame
df = pd.read_sql_query(query, conn)
# Convertir la columna 'fecha' a tipo de dato de fecha
df['fecha'] = pd.to_datetime(df['fecha'])

# Calcular la media y la desviación estándar de las fechas
media_fechas = df['fecha'].mean()
desviacion_fechas = df['fecha'].std()

print("Apartado 2")
print("Media de fechas detectadas:", media_fechas)
print("Desviación estándar de las fechas detectadas:", desviacion_fechas)


# Apartado 3:
total_ips = df['ip'].nunique()
media_ips = total_ips / len(df)  # La media es el total de IPs únicas dividido por el total de registros
desviacion_ips = np.sqrt(((df['ip'].value_counts() - media_ips) ** 2).sum() / len(df))  # La desviación estándar
print("Apartado 3")
print("Media de IPs:", media_ips)
print("Desviación estándar de IPs :", desviacion_ips)

#Apartado 4:
print("Apartado 4")
query1 = """
    SELECT SUM(cliclados_emails) AS total_phishing_emails
    FROM users 
"""
df = pd.read_sql_query(query1, conn)
sumaTotal = df['total_phishing_emails'].iloc[0]
print("Media de clicados : "+str(sumaTotal/num_muestras))

query2=query = """
    SELECT cliclados_emails
    FROM users 
"""
df2 = pd.read_sql_query(query2, conn)
desviacion=df2['cliclados_emails'].std()
print("Desviacion tipica clicados : "+str(desviacion))

#Apartado 5:
print("Apartado 5")
query = """
    SELECT MIN(total_emails) AS min_total_emails, MAX(total_emails) AS max_total_emails
    FROM users
"""

df=pd.read_sql_query(query,conn)
min_total_emails = df['min_total_emails'].iloc[0]
max_total_emails = df['max_total_emails'].iloc[0]

print("Valor mínimo del total de emails recibidos:", min_total_emails)
print("Valor máximo del total de emails recibidos:", max_total_emails)


#Apartado 6:
print("Apartado 6")
query = """
    SELECT MIN(cliclados_emails) AS min_emails, MAX(cliclados_emails) AS max_emails
    FROM users WHERE permisos=1
"""

df=pd.read_sql_query(query,conn)
min_total_emails = df['min_emails'].iloc[0]
max_total_emails = df['max_emails'].iloc[0]

print("Numero mínimo  emails interactuados admin:", min_total_emails)
print("Numero máximo  emails interactuados admin:", max_total_emails)

'''
# Consulta para obtener las fechas de cambio de contraseña por usuario
query = """
    SELECT u.username, u.permisos, ui.fecha
    FROM users u
    INNER JOIN user_ips ui ON u.username = ui.username
    WHERE u.contrasena IS NOT NULL
"""

# Leer los datos de la consulta en un DataFrame
df = pd.read_sql_query(query, conn)

# Convertir la columna 'fecha' al tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Calcular la diferencia de tiempo entre cambios de contraseña para cada usuario
df['diferencia'] = df.groupby('username')['fecha'].diff().dt.days

# Separar usuarios normales de administradores
usuarios_normales = df[df['permisos'] == 0]
usuarios_administradores = df[df['permisos'] == 1]

# Calcular la media de tiempo entre cambios de contraseña para usuarios normales y administradores
media_tiempo_normales = usuarios_normales['diferencia'].mean()
media_tiempo_administradores = usuarios_administradores['diferencia'].mean()

print("Media de tiempo entre cambios de contraseña para usuarios normales:", media_tiempo_normales)
print("Media de tiempo entre cambios de contraseña para usuarios administradores:", media_tiempo_administradores)
'''
# Consulta para obtener los datos necesarios
query = """
    SELECT web, 
       SUM(cookies) AS Cookies_0,
       SUM(aviso) AS Aviso_0,
       SUM(proteccion_de_datos) AS Protección_de_datos_0
FROM legal
GROUP BY web
ORDER BY Cookies_0 ASC, Aviso_0 ASC, Protección_de_datos_0 ASC

"""
'''
# Leer los datos en un DataFrame, asegurándose de que la columna de fecha se parsea correctamente
df = pd.read_sql_query(query, conn)
print(df)
'''

df = pd.read_sql_query(query, conn)

df['Total_desactualizadas'] = df['Cookies_0'] + df['Aviso_0'] + df['Protección_de_datos_0']

# Ordena el DataFrame por la columna Total_desactualizadas en orden descendente
df = df.sort_values(by='Total_desactualizadas', ascending=True)

# Toma las primeras 5 filas (las 5 páginas web con más políticas desactualizadas)
top_5 = df.head()

# Crea el gráfico de barras
plt.bar(top_5['web'], top_5['Total_desactualizadas'])
plt.xlabel('Página Web')
plt.ylabel('Número total de políticas desactualizadas')
plt.title('Las 5 páginas web con más políticas desactualizadas')
plt.xticks(rotation=45)  # Rotar etiquetas del eje x para mayor legibilidad
plt.tight_layout()  # Ajustar el diseño
plt.show()