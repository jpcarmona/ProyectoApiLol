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
		lista=[]
	else:
		nombre =request.form.get("nombre")
		region =request.form.get("region")
		plantilla,lista,session['idinvocador']=get_fullinfo(apikey,nombre,region)
		session['lista']=lista
	return render_template(plantilla,lista=lista)

@app.route('/perfil',methods=["post","get"])
def perfil():
	if session['lista']:
		plantilla ='perfil.html'
		lista=session['lista']
	else:
		plantilla =('index.html')
		lista=[]
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

