import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('BBDD.db')
def obtenerDataQuery():
    # Conectarse a la base de datos
    conn = sqlite3.connect('BBDD.db')
    query1 = "SELECT COUNT(*) AS num_muestras FROM users"
    query2 = "SELECT ip, fecha FROM user_ips"
    query3 = "SELECT SUM(cliclados_emails) AS total_phishing_emails FROM users "

    df1=pd.read_sql_query(query1,conn)
    df2=pd.read_sql_query(query2,conn)
    df3=pd.read_sql_query(query3,conn)

    resultado={
        'num_muestras':df1['num_muestras'].iloc[0]
    }

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
