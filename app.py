import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import sqlite3
import hashlib
import Ejercicio2
import Ejercicio3
import Ejercicio3Practica2
import Ejercicio4
import matplotlib

import Ejercicio5Clasificadores
import Ejercicio4Practica2

app = Flask(__name__)
conn = sqlite3.connect('BBDD.db')
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ejercicio2")
def ejercicio2():
    num_muestras=Ejercicio2.apartado_1()
    media_fechas,desviacion_fechas=Ejercicio2.apartado_2()
    medias_ips,desviacion_ips=Ejercicio2.apartado_3()
    media_emails_recibidos,desviacion_emails_recibidos=Ejercicio2.apartado_4()
    min_emails_recibidos,max_emails_recibidos=Ejercicio2.apartado_5()
    min_emails_admin,max_emails_admin=Ejercicio2.apartado_6()
    return render_template('ejercicio2.html',num_muestras=num_muestras,media_fechas=media_fechas,
                           desviacion_fechas=desviacion_fechas,medias_ips=medias_ips,desviacion_ips=desviacion_ips,
                           media_emails_recibidos=media_emails_recibidos,desviacion_emails_recibidos=desviacion_emails_recibidos,
                           min_emails_recibidos=min_emails_recibidos,max_emails_recibidos=max_emails_recibidos,min_emails_admin=min_emails_admin,
                           max_emails_admin=max_emails_admin)

@app.route("/ejercicio3")  # Ruta para el ejercicio 3
def ejercicio3():
    # Obtener estadísticas desde Ejercicio3
    stats_correos, stats_contrasenas = Ejercicio3.estadisticas()
    cont_campos_vacios_usuarios, cont_campos_vacios_admin = Ejercicio3.obtener_usuarios_campos_vacios()

    # Renderizar la plantilla HTML y pasar los datos
    return render_template('ejercicio3.html', stats_correos=stats_correos, stats_contrasenas=stats_contrasenas,
                           cont_campos_vacios_usuarios=cont_campos_vacios_usuarios,
                           cont_campos_vacios_admin=cont_campos_vacios_admin)


@app.route('/ejercicio4')
def ejercicio4_route():
    datos = Ejercicio4.obtener_datos_ejercicio4()
    return render_template('ejercicio4.html',datos=datos)

@app.route('/consulta-ejer-1', methods=['GET'])
def mostrar_formulario():
    return render_template('EleccionE1.html')

@app.route('/consulta-usuarios-criticos', methods=['GET'])
def mostrar_formulario2():
    return render_template('Ejercicio1P2.html')


@app.route('/Ejercicio1P2', methods=['GET'])
def consultar_usuarios_criticos():
    if request.method == 'GET':
        num_usuarios_criticos = int(request.args.get('num_usuarios_criticos'))
        resultados = Ejercicio4.obtener_usuarios_criticos(num_usuarios_criticos)
        return render_template('resultados_usuarios_criticos.html', resultados=resultados)

@app.route('/consulta-paginas-desactualizadas', methods=['GET'])
def mostrar_formulario_paginas_desactualizadas():
    return render_template('formulario_paginas_desactualizadas.html')

@app.route('/consultar-paginas-desactualizadas', methods=['GET'])
def consultar_paginas_desactualizadas():
    if request.method == 'GET':
        num_paginas_desactualizadas = int(request.args.get('num_paginas_desactualizadas'))
        paginas_desactualizadas = Ejercicio4.obtener_top_paginas_desactualizadas(num_paginas_desactualizadas)
        return render_template('resultados_paginas_desactualizadas.html', paginas_desactualizadas=paginas_desactualizadas)


@app.route('/Ejercicio3P2')
def mostrar_vulnerabilidades():
    vulnerabilidades = Ejercicio3Practica2.obtener_ultimas_vulnerabilidades()
    if vulnerabilidades:
        return render_template('Ejercicio3P2.html', vulnerabilidades=vulnerabilidades)
    else:
        return "Error al obtener las vulnerabilidades"

@app.route('/consulta-ejer-5', methods=['GET'])
def eleccion_modelo():
    return render_template('EleccionE5.html')
@app.route('/regresionLineal', methods=['GET'])
def regresionLinealForm():
    return render_template('formularioRegresionLineal.html')

@app.route('/devolverAnalisisRegresionLineal', methods=['GET'])
def regresionLineal():
    if request.method=='GET':
        nombre=(request.args.get('nombre'))
        telefono=(request.args.get('telefono'))
        provincia=(request.args.get('provincia'))
        #permisos=request.form['permisos']
        total_enviados=(request.args.get('total_enviados'))
        phishing=(request.args.get('phishing'))
        clicados=(request.args.get('clicados'))

        usuario=(nombre,telefono,provincia,total_enviados,phishing,clicados)
        emails=(total_enviados,phishing,clicados)
        resultado=Ejercicio5Clasificadores.regresionLineal(emails)
        print(resultado)
        return render_template('resultados_clasificador',usuario=usuario,resultado=resultado)


@app.route('/Ejercicio4P2')
def ejercicio4_p2():
    return render_template('Ejercicio4P2.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('formulario_registro.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fecha = request.form.get('fecha')
        Ejercicio4Practica2.registrar_usuario(username, password, fecha)
        return redirect(url_for('index'))

@app.route('/iniciar', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('formulario_login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Ejercicio4Practica2.iniciar_sesion(username, password)
        return redirect(url_for('index'))

@app.route('/conexiones')
def conexiones():
    query = "SELECT username, fecha FROM usuarioslogin"
    df = pd.read_sql_query(query, conn)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['dia'] = df['fecha'].dt.date
    conexiones_por_dia = df.groupby(['dia', 'username']).size().reset_index(name='conexiones')
    return render_template('conexiones.html', conexiones_por_dia=conexiones_por_dia)

if __name__ == '__main__':
    app.run(debug=True)


