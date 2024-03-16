
import pandas as pd
import numpy as np
import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('BBDD.db')

#Ejercicio 1:
query="SELECT COUNT(*) AS num_muestras FROM users"
df = pd.read_sql_query(query, conn)
num_muestras = df['num_muestras'].iloc[0]  # Obtener el valor de 'num_muestras' de la primera fila
print("Ejericicio 1")
print("Número total de muestras:", num_muestras)

#Ejercicio 2:
query = "SELECT ip, fecha FROM user_ips"
df = pd.read_sql_query(query, conn)
total_fecha=df['fecha'].nunique()
media_fechas = total_fecha / len(df)  # La media es el total de fechas únicas dividido por el total de registros
desviacion_fechas = np.sqrt(((df['ip'].value_counts() - media_fechas) ** 2).sum() / len(df))  # La desviación estándar
print("Ejercicio 2")
print("Media de IPs detectadas:", media_fechas)
print("Desviación estándar de IPs detectadas:", desviacion_fechas)

# Ejercicio 3:
total_ips = df['ip'].nunique()
media_ips = total_ips / len(df)  # La media es el total de IPs únicas dividido por el total de registros
desviacion_ips = np.sqrt(((df['ip'].value_counts() - media_ips) ** 2).sum() / len(df))  # La desviación estándar
print("Ejercicio 3")
print("Media de fechas:", media_ips)
print("Desviación estándar de fechas :", desviacion_ips)

#Ejercicio 4:
query = """
    SELECT SUM(cliclados_emails) AS total_phishing_emails
    FROM users 
"""
df = pd.read_sql_query(query, conn)
sumaTotal = df['total_phishing_emails'].iloc[0]
print("Media de clicados : "+str(sumaTotal/num_muestras))

'''
desviacion_estandar = df['total_phishing_emails'].std()

print("Media de correos electrónicos de phishing recibidos por usuario:", sumaTotal)
print("Desviación estándar de correos electrónicos de phishing recibidos por usuario:", desviacion_estandar)'''

