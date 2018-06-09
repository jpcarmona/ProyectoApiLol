from flask import Flask, url_for, render_template, request, session
from funciones import *
import os


app = Flask(__name__)
#app.secret_key="sdhaksjhdkasjdhsakjddksa"
app.secret_key=str(os.system("openssl rand -base64 24"))
port = os.environ['PORT']
apikey=get_apikey()
#save_champions(apikey)

@app.route('/',methods=["post","get"])
def inicio():	
	if request.method == "GET":
		plantilla =('index.html')
		region='euw1'
		gratuitos=get_freechampions(apikey,region)
		lista=[gratuitos,0]
	else:
		session.clear()
		nombre =request.form.get("nombre")
		region =request.form.get("region")
		plantilla,lista=get_fullinfo(apikey,nombre,region)
		if lista[1]!=1:
			session['idinvocador']=lista[0]['id']
			session['lista']=lista
	return render_template(plantilla,lista=lista)

@app.route('/perfil',methods=["post","get"])
def perfil():
	if session:
		plantilla ='perfil.html'
		lista=session['lista']
	else:
		plantilla =('index.html')
		region='euw1'
		gratuitos=get_freechampions(apikey,region)
		lista=[gratuitos,0]
	return render_template(plantilla,lista=lista)

@app.route('/historial',methods=["post","get"])
def historial():
	if request.method == "GET":
		return render_template('historial.html')

@app.route('/maestrias',methods=["post","get"])
def maestrias():
	if request.method == "GET":
		return render_template('maestrias.html')

app.run('0.0.0.0',int(port), debug=True)

