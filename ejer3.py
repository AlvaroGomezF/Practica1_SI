import sqlite3
import hashlib
import pandas as pd

# Configuración para mostrar todas las columnas y ancho completo
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def obtener_datos():
    # Conexión a la base de datos
    conn = sqlite3.connect('BBDD.db')

    # Consultas SQL para obtener datos relevantes
    consulta_contrasenas = "SELECT contrasena, phishing_emails FROM users"
    consulta_correos = "SELECT permisos, phishing_emails FROM users"

    # Lectura de datos desde la base de datos
    contrasenas = pd.read_sql_query(consulta_contrasenas, conn)
    correos = pd.read_sql_query(consulta_correos, conn)

    # Cierre de la conexión a la base de datos
    conn.close()

    return contrasenas, correos

def calcular_hashes(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        hashed_passwords = set(hashlib.md5(passwd.encode()).hexdigest() for passwd in passwords)
    return hashed_passwords

def comparar_hashes(hashes_base_datos, hashes_diccionario):
    resultado = []

    for i in hashes_base_datos:
        if i in hashes_diccionario:
            resultado.append("Debil")
        else:
            resultado.append("Fuerte")

    return resultado

def calcular_valores_ausentes(df):
    valores_ausentes = df['phishing_emails'].isnull().astype(int)
    return valores_ausentes

def estadisticas():
    # Obtener datos de la base de datos
    contrasenas, correos = obtener_datos()

    # Calcular hashes de contraseñas
    hashes_sry = calcular_hashes('SRY.txt')

    # Calcular dificultad de las contraseñas
    contrasenas['dificultad'] = comparar_hashes(contrasenas['contrasena'], hashes_sry)

    # Convertir permisos a tipo entero
    correos['permisos'] = correos['permisos'].astype(int)

    # Calcular valores ausentes para correos y contraseñas
    correos['perdido'] = calcular_valores_ausentes(correos)
    contrasenas['perdido'] = calcular_valores_ausentes(contrasenas)
    # Calcular estadísticas para correos
    stats_correos = correos.groupby('permisos')['phishing_emails'].agg(
        ['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Número de observaciones',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })
    # Calcular la suma de valores nulos
    valores_nulos_correos = correos.groupby('permisos')['perdido'].sum()
    valores_nulos_contrasenas = contrasenas.groupby('dificultad')['perdido'].sum()



    # Calcular estadísticas para contraseñas
    stats_contrasenas = contrasenas.groupby('dificultad')['phishing_emails'].agg(
        ['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Número de observaciones',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })

    # Agregar columnas de valores ausentes a las estadísticas
    stats_correos['Número de valores ausentes (missing)'] = valores_nulos_correos
    stats_contrasenas['Número de valores ausentes (missing)'] = valores_nulos_contrasenas

    # Redondear los valores estadísticos
    stats_correos = stats_correos.round(4)
    stats_contrasenas = stats_contrasenas.round(4)

    return stats_correos, stats_contrasenas

# Obtener estadísticas
stats_correos, stats_contrasenas = estadisticas()

# Imprimir las estadísticas para los correos
print("Estadísticas para usuarios (phishing_emails):")
print(stats_correos)
print()

# Imprimir las estadísticas para las contraseñas
print("Estadísticas para contraseñas:")
print(stats_contrasenas)
