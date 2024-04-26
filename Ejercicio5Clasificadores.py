import sqlite3

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

conn = sqlite3.connect('BBDD.db')

def regresionLineal(nuevoDato):

    # Datos de ejemplo (sustituye esto con tus datos reales)
    # Aquí deberías cargar tus datos desde la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)
    print(df.head())

    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        caracteristicas.append([row["total_emails"], row["phising_emails"], row["ciclado_emails"]])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Evaluar el modelo
    precision = modelo.score(X_test, y_test)
    print("Precisión del modelo:", precision)
    precision = modelo.predict(nuevoDato)
    return precision[0]

def decision_tree():
    # Datos de ejemplo (sustituye esto con tus datos reales)
    # Aquí deberías cargar tus datos desde la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)
    print(df.head())

    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        caracteristicas.append([row["total_emails"], row["phising_emails"], row["ciclado_emails"]])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instanciar y entrenar el modelo de árbol de decisión
    modelo = DecisionTreeClassifier()
    modelo.fit(X_train, y_train)

    # Evaluar el modelo
    precision = modelo.score(X_test, y_test)
    print("Precisión del modelo:", precision)

def random_forest(nuevoDato):
    # Datos de ejemplo (sustituye esto con tus datos reales)
    # Aquí deberías cargar tus datos desde la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)
    print(df.head())

    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        caracteristicas.append([row["total_emails"], row["phising_emails"], row["ciclado_emails"]])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Instanciar y entrenar el modelo de árbol de decisión
    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    # Evaluar el modelo
    precision = modelo.score(X_test, y_test)
    print("Precisión del modelo:", precision)

    precision=modelo.predict(nuevoDato)
    if precision[0]==1:
        print("El nuevo dato es critico")
    else:
        print("El nuevo dato no es critico")


#decision_tree()
#nuevoDato=[[10,2,1]]
#regresionLineal(nuevoDato)