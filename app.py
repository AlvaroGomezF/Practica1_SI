import json
from flask import Flask, render_template, request, redirect, url_for
import Ejercicio2
import Ejercicio3
import Ejercicio4
import matplotlib
app = Flask(__name__)


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

@app.route('/consulta-usuarios-criticos', methods=['GET'])
def mostrar_formulario():
    return render_template('Ejercicio1P2.html')


@app.route('/Ejercicio1P2', methods=['GET'])
def consultar_usuarios_criticos():
    if request.method == 'GET':
        num_usuarios_criticos = int(request.args.get('num_usuarios_criticos'))
        resultados = Ejercicio4.obtener_usuarios_criticos(num_usuarios_criticos)
        return render_template('resultados_usuarios_criticos.html', resultados=resultados)
