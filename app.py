import json
from flask import Flask, render_template, request, redirect, url_for
import Ejercicio2
import Ejercicio3
import Ejercicio4
import matplotlib
app = Flask(_name_)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ejercicio2")
def ejercicio2():
    df_results=ejercicio2.obtenerDataQuery()


@app.route("/ejercicio3")  # Ruta para el ejercicio 3
def ejercicio3():
    # Obtener estadísticas desde Ejercicio3
    stats_correos, stats_contrasenas = Ejercicio3.estadisticas()
    cont_campos_vacios_usuarios, cont_campos_vacios_admin = Ejercicio3.obtener_usuarios_campos_vacios()

    # Renderizar la plantilla HTML y pasar los datos
    return render_template('ejercicio3.html', stats_correos=stats_correos, stats_contrasenas=stats_contrasenas,
                           cont_campos_vacios_usuarios=cont_campos_vacios_usuarios,
                           cont_campos_vacios_admin=cont_campos_vacios_admin)