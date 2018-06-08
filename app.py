from flask import Flask, url_for, render_template, request, session
from funciones import *
import os

app = Flask(__name__)
port = os.environ['PORT']

apikey=get_apikey()
#save_champions(apikey)

@app.route('/',methods=["post","get"])
def inicio():
	if request.method == "GET":
		plantilla =('index.html')
		lista=[]
	else:
		nombre =request.form.get("nombre")
		region =request.form.get("region")
		doc_info =get_info(apikey,nombre,region)
		if doc_info:
			doc_info['liga']=get_liga(apikey,doc_info['id'],region)
			doc_actual =get_actual(apikey,doc_info['id'],region)
			plantilla =('perfil.html')
			partida={}
			if doc_actual:
				partida =partida_actual(doc_actual['participants'],apikey,region)
			lista=[doc_info,doc_actual,partida]
		else:
			plantilla =('index.html')
			lista=[1]
	return render_template(plantilla,lista=lista)

@app.route('/perfil',methods=["post","get"])
def perfil():
	if request.method == "GET":
		return render_template('perfil.html')

@app.route('/historial',methods=["post","get"])
def historial():
	if request.method == "GET":
		return render_template('historial.html')

@app.route('/maestrias',methods=["post","get"])
def maestrias():
	if request.method == "GET":
		return render_template('maestrias.html')
		

app.run('0.0.0.0',int(port), debug=True)

