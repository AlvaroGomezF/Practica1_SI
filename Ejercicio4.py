import hashlib
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import io
import base64

def obtener_usuarios_criticos(num_usuarios_criticos):
    conn = sqlite3.connect('BBDD.db')
    query1 = '''
    SELECT username, contrasena
    FROM users
    '''
    query2 = '''
    SELECT username, phishing_emails, cliclados_emails
    FROM users
    '''
    dfUsuarios = pd.read_sql_query(query1, conn)
    dfCorreos = pd.read_sql_query(query2, conn)

    dfCorreos['probabilidad'] = dfCorreos['cliclados_emails'] / dfCorreos['phishing_emails']
    hashes_sry = calcular_hashes('SRY.txt')
    dfUsuarios['robustez'] = compararHashes(dfUsuarios['contrasena'], hashes_sry)
    usuariosDebiles = dfUsuarios[dfUsuarios['robustez'] == 'Debil']

    usuariosMasCriticos = usuariosDebiles.merge(dfCorreos, on='username')

    usuarios_criticos = usuariosMasCriticos.nlargest(num_usuarios_criticos, 'probabilidad')

    return usuarios_criticos



def calcular_hashes(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        hashed_passwords = set(hashlib.md5(passwd.encode()).hexdigest() for passwd in passwords)
    return hashed_passwords

def compararHashes(hashes_bd, hashes_dicc):
    resultado = []

    for i in hashes_bd:
        if i in hashes_dicc:
            resultado.append("Debil")
        else:
            resultado.append("Fuerte")
    return resultado

def obtener_grafico_barras_media_tiempo(media_tiempo_normales, media_tiempo_administradores):
    plt.figure()
    listasMedias = [media_tiempo_normales, media_tiempo_administradores]
    listaCat = ['Usuarios Normales', 'Usuarios Admin']
    plt.bar(listaCat, listasMedias, color=['yellow', 'red'])
    plt.title('Media de tiempo de cambio de contraseña por Tipo de Usuario')
    plt.xlabel('Tipo de Usuario')
    plt.ylabel('Media de Tiempo')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64


import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import base64
import io


def obtener_grafico_usuarios_criticos(conn):
    query1 = '''
    SELECT username, contrasena FROM users
    '''
    query2 = '''
    SELECT username, phishing_emails, cliclados_emails FROM users
    '''

    # Ejecutar las consultas SQL y guardar los resultados en DataFrames
    df_usuarios = pd.read_sql_query(query1, conn)
    df_correos = pd.read_sql_query(query2, conn)

    # Calcular la probabilidad de los usuarios
    df_correos['probabilidad'] = df_correos['cliclados_emails'] / df_correos['phishing_emails']

    # Calcular la robustez de las contraseñas de los usuarios
    hashes_sry = calcular_hashes('SRY.txt')
    df_usuarios['robustez'] = compararHashes(df_usuarios['contrasena'], hashes_sry)

    # Filtrar los usuarios con contraseñas débiles
    usuarios_debiles = df_usuarios[df_usuarios['robustez'] == 'Debil']

    # Unir los DataFrames para obtener los usuarios con mayor criticidad
    usuarios_criticos = usuarios_debiles.merge(df_correos, on='username')

    # Obtener los 10 usuarios con mayor probabilidad de cliclados de emails phishing
    usuarios_top_10 = usuarios_criticos.nlargest(10, 'probabilidad')

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.barh(usuarios_top_10['username'], usuarios_top_10['probabilidad'], color='skyblue')
    plt.xlabel('Probabilidad')
    plt.ylabel('Usuarios')
    plt.title('Usuarios con mayor criticidad')
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convertir la imagen a base64
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64


def obtener_grafico_barras_webs_buenas_malas(conn):
    query = '''
    SELECT creacion AS año,
           SUM(CASE WHEN cookies = 1 AND aviso = 1 AND proteccion_de_datos = 1 THEN 1 ELSE 0 END) AS añosBueno,
           SUM(CASE WHEN cookies = 0 OR aviso = 0 OR proteccion_de_datos = 0 THEN 1 ELSE 0 END) AS añosMalo
    FROM legal
    GROUP BY creacion
    '''

    df = pd.read_sql_query(query, conn)

    todos_los_años = pd.DataFrame({'año': range(2000, 2024)})

    df = todos_los_años.merge(df, on='año', how='left').fillna(0)

    ancho_barra = 0.4
    plt.bar(df['año'] - ancho_barra/2, df['añosBueno'], width=ancho_barra, color='green', label='Buenos')
    plt.bar(df['año'] + ancho_barra/2, df['añosMalo'], width=ancho_barra, color='red', label='Malos')

    plt.xlabel('Año de Creación')
    plt.ylabel('Cantidad de Webs')
    plt.title('Cantidad de Webs Buenas y Malas por Año de Creación')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64


def obtener_grafico_politicas_por_web(conn):
    query = '''
    SELECT web, cookies, aviso, proteccion_de_datos, creacion
    FROM legal
    '''

    # Ejecutar la consulta SQL y guardar los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)

    # Calcular el total de políticas para cada página web
    df['total'] = df['cookies'] + df['aviso'] + df['proteccion_de_datos']

    # Seleccionar las 5 páginas web con menos políticas
    paginas_top_5 = df.nsmallest(5, 'total')

    # Configurar los datos para el gráfico de barras
    web_creacion = paginas_top_5['web'] + ' (' + paginas_top_5['creacion'].astype(str) + ')'
    cookies = paginas_top_5['cookies']
    aviso = paginas_top_5['aviso']
    proteccion_de_datos = paginas_top_5['proteccion_de_datos']

    x = range(len(web_creacion))

    # Dibujar el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(x, cookies, width=0.2, label='Cookies')
    plt.bar([i + 0.2 for i in x], aviso, width=0.2, label='Aviso')
    plt.bar([i + 0.4 for i in x], proteccion_de_datos, width=0.2, label='Protección de Datos')

    plt.xlabel('Páginas Web')
    plt.ylabel('Número de Políticas')
    plt.title('Políticas por Página Web')
    plt.xticks([i + 0.2 for i in x], web_creacion)
    plt.legend()
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convertir la imagen a base64
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64

def obtener_grafico_media_anos_creacion(conn):
    query = '''
    SELECT creacion,
           AVG(CASE WHEN cookies = 1 AND aviso = 1 AND proteccion_de_datos = 1 THEN creacion ELSE NULL END) AS media_anos_bueno,
           AVG(CASE WHEN cookies = 0 OR aviso = 0 OR proteccion_de_datos = 0 THEN creacion ELSE NULL END) AS media_anos_malo
    FROM legal
    GROUP BY creacion
    '''

    # Ejecutar la consulta y guardar los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)

    # Configurar los datos para el gráfico de barras
    lista_anos = df['creacion']
    lista_media_anos_bueno = df['media_anos_bueno']
    lista_media_anos_malo = df['media_anos_malo']

    # Crear el gráfico de barras
    plt.bar(lista_anos, lista_media_anos_bueno, color='green', label='Cumplen políticas')
    plt.bar(lista_anos, lista_media_anos_malo, color='red', label='No cumplen políticas')

    plt.xlabel('Año de Creación')
    plt.ylabel('Media de Años de Creación')
    plt.title('Media de Años de Creación según Cumplimiento de Políticas')
    plt.legend()
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para una mejor visualización

    # Guardar la gráfica en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convertir la imagen a base64
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64
def obtener_datos_ejercicio4():
    conn = sqlite3.connect('BBDD.db')

    query = """
        SELECT u.username, u.permisos, ui.fecha
        FROM users u
        INNER JOIN user_ips ui ON u.username = ui.username
        WHERE u.contrasena IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    df_sorted = df.sort_values(by=['username', 'fecha'])

    df_sorted['diferencia'] = df_sorted.groupby('username')['fecha'].diff().dt.days

    usuarios_normales = df_sorted[df_sorted['permisos'] == 0]
    usuarios_administradores = df_sorted[df_sorted['permisos'] == 1]

    media_tiempo_normales = usuarios_normales['diferencia'].mean()
    media_tiempo_administradores = usuarios_administradores['diferencia'].mean()

    grafico_politicas = obtener_grafico_politicas_por_web(conn)
    grafico_media_tiempo = obtener_grafico_barras_media_tiempo(media_tiempo_normales, media_tiempo_administradores)
    grafico_usuarios_criticos = obtener_grafico_usuarios_criticos(conn)
    grafico_webs_buenas_malas = obtener_grafico_barras_webs_buenas_malas(conn)
    grafica_media_anos_creacion = obtener_grafico_media_anos_creacion(conn)

    return {
        'media_tiempo_normales': media_tiempo_normales,
        'media_tiempo_administradores': media_tiempo_administradores,
        'grafico_media_tiempo': grafico_media_tiempo,
        'grafico_webs_buenas_malas': grafico_webs_buenas_malas,
        'grafico_usuarios_criticos':grafico_usuarios_criticos,
        'grafico_politicas_por_web': grafico_politicas,
        'grafico_media_anos_creacion': grafica_media_anos_creacion,
    }