import pandas as pd
import numpy as np
import sqlite3
def apartado_1():
    conn = sqlite3.connect('BBDD.db')
    query = "SELECT COUNT(*) AS num_muestras FROM users"
    df = pd.read_sql_query(query, conn)
    num_muestras = df['num_muestras'].iloc[0]
    return num_muestras
def apartado_2():
    conn = sqlite3.connect('BBDD.db')
    query = "SELECT ip, fecha FROM user_ips"
    df = pd.read_sql_query(query, conn)
    df['fecha'] = pd.to_datetime(df['fecha'])
    media_fechas = df['fecha'].mean()
    desviacion_fechas = df['fecha'].std()
    return media_fechas,desviacion_fechas

def apartado_3():
    conn = sqlite3.connect('BBDD.db')
    query = "SELECT ip FROM user_ips"
    df = pd.read_sql_query(query, conn)
    total_ips = df['ip'].nunique()
    media_ips = total_ips / len(df)
    desviacion_ips = np.sqrt(((df['ip'].value_counts() - media_ips) ** 2).sum() / len(df))
    return media_ips,desviacion_ips
def apartado_4():
    conn = sqlite3.connect('BBDD.db')

    query = "SELECT SUM(cliclados_emails) AS total_phishing_emails FROM users"
    df = pd.read_sql_query(query, conn)
    sumaTotal = df['total_phishing_emails'].iloc[0]
    query = "SELECT cliclados_emails FROM users"
    df2 = pd.read_sql_query(query, conn)
    desviacion_clicados = df2['cliclados_emails'].std()
    return sumaTotal/apartado_1(),desviacion_clicados

def apartado_5():
    conn = sqlite3.connect('BBDD.db')
    query = "SELECT MIN(total_emails) AS min_total_emails, MAX(total_emails) AS max_total_emails FROM users"
    df = pd.read_sql_query(query, conn)
    min_total_emails = df['min_total_emails'].iloc[0]
    max_total_emails = df['max_total_emails'].iloc[0]
    return min_total_emails,max_total_emails

def apartado_6():
    conn = sqlite3.connect('BBDD.db')
    query = "SELECT MIN(cliclados_emails) AS min_emails, MAX(cliclados_emails) AS max_emails FROM users WHERE permisos=1"
    df = pd.read_sql_query(query, conn)
    min_emails_admin = df['min_emails'].iloc[0]
    max_emails_admin = df['max_emails'].iloc[0]
    return min_emails_admin,max_emails_admin