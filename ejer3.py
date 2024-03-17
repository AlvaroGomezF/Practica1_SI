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

# Funcion para obtener los usuarios con algun campo vacio
def obtener_usuarios_campos_vacios():
    conn = sqlite3.connect('BBDD.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(DISTINCT username) FROM users WHERE (telefono='None' OR contrasena='None' OR provincia='None') AND permisos=0")
    cont_campos_vacios_usuarios = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT username) FROM users WHERE (telefono='None' OR contrasena='None' OR provincia='None') AND permisos=1")
    cont_campos_vacios_admin = c.fetchone()[0]

    conn.close()

    return cont_campos_vacios_usuarios, cont_campos_vacios_admin

# Funcion para calcular los hashes de las contraseñas almacenadas en un archivo de texto
def calcular_hashes(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        hashed_passwords = set(hashlib.md5(passwd.encode()).hexdigest() for passwd in passwords)
    return hashed_passwords

# Funcion para comparar los hashes de las contraseñas almacenadas en la BBDD
# con los hashes del diccionario
def comparar_hashes(hashes_bbdd, hashes_diccionary):
    resultado = []

    for i in hashes_bbdd:
        if i in hashes_diccionary:
            resultado.append("Debil")
        else:
            resultado.append("Fuerte")

    return resultado

def estadisticas():
    # Obtener datos de la base de datos
    contrasenas, correos = obtener_datos()

    # Calcular hashes de contraseñas
    hashes_sry = calcular_hashes('SRY.txt')

    # Calcular dificultad de las contraseñas
    contrasenas['Robustez'] = comparar_hashes(contrasenas['contrasena'], hashes_sry)

    # Convertir permisos a tipo entero
    correos['Rol'] = correos['permisos'].replace({0: 'Usuario', 1: 'Administrador'})

    # Calcular estadísticas para correos
    stats_correos = correos.groupby('Rol')['phishing_emails'].agg(
        ['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Cantidad',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })

    # Calcular estadísticas para contraseñas
    stats_contrasenas = contrasenas.groupby('Robustez')['phishing_emails'].agg(
        ['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Cantidad',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })

    # Redondear los valores estadísticos
    stats_correos = stats_correos.round(2)
    stats_contrasenas = stats_contrasenas.round(2)

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

cont_campos_vacios_usuarios , cont_campos_vacios_admin= obtener_usuarios_campos_vacios()
print("\n")
print("Número de usuarios con campos vacíos: " + str(cont_campos_vacios_usuarios))
print("Número de administradores con campos vacíos: " + str(cont_campos_vacios_admin))


