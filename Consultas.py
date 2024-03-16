
import pandas as pd
import numpy as np
import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('BBDD.db')

#Ejercicio 1:
query="SELECT COUNT(*) AS num_muestras FROM users"
df = pd.read_sql_query(query, conn)
num_muestras = df['num_muestras'].iloc[0]  # Obtener el valor de 'num_muestras' de la primera fila
print("Apartado 1")
print("Número total de muestras:", num_muestras)

#Ejercicio 2:
query = "SELECT ip, fecha FROM user_ips"
df = pd.read_sql_query(query, conn)
total_fecha=df['fecha'].nunique()
media_fechas = total_fecha / len(df)  # La media es el total de fechas únicas dividido por el total de registros
desviacion_fechas = np.sqrt(((df['ip'].value_counts() - media_fechas) ** 2).sum() / len(df))  # La desviación estándar
print("Apartado 2")
print("Media de IPs detectadas:", media_fechas)
print("Desviación estándar de IPs detectadas:", desviacion_fechas)

# Ejercicio 3:
total_ips = df['ip'].nunique()
media_ips = total_ips / len(df)  # La media es el total de IPs únicas dividido por el total de registros
desviacion_ips = np.sqrt(((df['ip'].value_counts() - media_ips) ** 2).sum() / len(df))  # La desviación estándar
print("Apartado 3")
print("Media de fechas:", media_ips)
print("Desviación estándar de fechas :", desviacion_ips)

#Ejercicio 4:
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

#Ejercicio 5:
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


#Ejercicio 6:
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
