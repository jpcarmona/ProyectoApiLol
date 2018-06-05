from flask import Flask, url_for, render_template, request, session
from funciones import *
import os

app = Flask(__name__)
port = os.environ['PORT']

apikey='RGAPI-0b9dffce-42bf-4d53-b6ca-94fbfdaff1f9'

@app.route('/',methods=["post","get"])
def inicio():
	if request.method == "GET":
		return render_template('index.html')
	else:
		nombre = request.form.get("nombre")
		region = request.form.get("region")
		doc_info = get_info(apikey,nombre,region)
		doc_actual = get_actual(apikey,doc_info['id'],region)
		jugadores = doc_actual['participants']
		return render_template('perfil.html',doc_info=doc_info,doc_actual=doc_actual,jugadores=jugadores)

@app.route('/historial',methods=["post","get"])
def historial():
	if request.method == "GET":
		return render_template('historial.html')

@app.route('/maestrias',methods=["post","get"])
def maestrias():
	if request.method == "GET":
		return render_template('maestrias.html')
		

app.run('0.0.0.0',int(port), debug=True)
