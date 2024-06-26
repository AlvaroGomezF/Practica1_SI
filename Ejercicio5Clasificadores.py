import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import clf
from pygments.lexers import graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import f1_score, accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import tree


def transformarNuevoDato(nuevoDato):

    if nuevoDato[0][1]==0:
        resultado=0
    else:
        resultado=nuevoDato[0][2]/nuevoDato[0][1]
    return [[resultado]]



def regresionLineal(nuevoDato):
    conn = sqlite3.connect('BBDD.db')

    #Cargamos los datos de la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)

    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        ciclado_emails = row['ciclado_emails']
        phising_emails = row['phising_emails']

        # Verificar si phising_emails es cero para evitar la división por cero
        if phising_emails != 0:
            proporcion_ciclado_phising = ciclado_emails / phising_emails
        else:
            # Si phising_emails es cero, asignar un valor predeterminado o manejar el caso según sea necesario
            proporcion_ciclado_phising = 0
        # Agregar la característica y etiqueta correspondiente
        caracteristicas.append([proporcion_ciclado_phising])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=4)

    # Entrenar el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    coef=modelo.coef_
    print("Coeficiente de regresion lineal",coef[0])
    datoTransformado=transformarNuevoDato(nuevoDato)

    y_pred=modelo.predict(X_test)
    print("Error regresion lineal:" ,mean_squared_error(y_pred,y_test))

    plt.figure(figsize=(10, 6))
    plt.scatter(X_test, y_test, color='blue', label='Datos de prueba')
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Línea de regresión')
    plt.title('Modelo de regresión lineal')
    plt.xlabel('Proporción ciclado/phising')
    plt.ylabel('Etiqueta crítica')
    plt.legend()
    plt.grid(True)
    plt.show()

    return modelo.predict(datoTransformado)>coef

def decision_tree(nuevoDato):
    conn = sqlite3.connect('BBDD.db')

    #Cargamos los datos de la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)


    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        caracteristicas.append([row["total_emails"], row["phising_emails"], row["ciclado_emails"],row['permisos']])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    # Instanciar y entrenar el modelo de árbol de decisión
    modelo = DecisionTreeClassifier()
    modelo.fit(X_train, y_train)

    y_pred=modelo.predict(X_test)
    # Evaluar el modelo
    precision2=accuracy_score(y_pred,y_test)
    print("Precision del modelo con .acurracy decision tree",precision2)

    # Imprimir el árbol de decisión
    plt.figure(figsize=(20, 10))
    plot_tree(modelo, filled=True, feature_names=["total_emails", "phising_emails", "ciclado_emails","permisos"],
              class_names=["No crítico", "Crítico"])
    plt.show()

    return modelo.predict(nuevoDato)


def random_forest(nuevoDato):
    conn = sqlite3.connect('BBDD.db')

    #Cargamos los datos de la base de datos
    query = """SELECT * FROM users_training"""
    df = pd.read_sql_query(query, conn)

    # Extraer características y etiquetas
    caracteristicas = []
    etiquetas = []
    for index, row in df.iterrows():
        caracteristicas.append([row["total_emails"], row["phising_emails"], row["ciclado_emails"],row['permisos']])
        etiquetas.append(row["critico"])

    # Convertir a matrices numpy
    X = np.array(caracteristicas)
    y = np.array(etiquetas)

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=36)

    # Instanciar y entrenar el modelo de árbol de decisión
    modelo = RandomForestClassifier(n_estimators=15,max_depth=2,random_state=10)
    modelo.fit(X_train, y_train)

    '''
    for i, arbol in enumerate(modelo.estimators_):
        plt.figure(figsize=(10, 6))
        tree.plot_tree(arbol, filled=True,
                       feature_names=["total_emails", "phising_emails", "ciclado_emails", "permisos"],
                       class_names=["No crítico", "Crítico"])
        plt.title(f"Árbol {i + 1}")
        plt.show()
    '''
    # Evaluar el modelo
    y_pred=modelo.predict(X_test)
    precision=accuracy_score(y_pred,y_test)
    print("Precision del modelo random forest: ",precision)

    return modelo.predict(nuevoDato)


#decision_tree()
nuevoDato=[[101,22,14,0]]
decision_tree(nuevoDato)

nuevoDato=[[100,100,90,1]]
regresionLineal(nuevoDato)

#random forest
nuevoDato=[[100,20,5,0]]
random_forest(nuevoDato)