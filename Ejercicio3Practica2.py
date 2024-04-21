import requests
from flask import Flask, render_template

app = Flask(__name__)

def obtener_ultimas_vulnerabilidades():
    url = "https://cve.circl.lu/api/last"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[:10]
    else:
        return None