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
    df_results=ejercicio2.obtenerData


