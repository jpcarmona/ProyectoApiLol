from flask import Flask, redirect, render_template, request, session
from funciones import *
import os

app = Flask(__name__)
app.secret_key=str(os.system('openssl rand -base64 24'))

port = os.environ['PORT']
apikey=get_apikey()
region='euw1' ## region por defecto
#save_champions(apikey,region)
#save_spells(apikey,region)


@app.route('/',methods=['POST','GET'])
def inicio():
	if 'region' in session:
		region=session['region']
	else:
		region='euw1'
	if request.method == 'GET':
		plantilla =('index.html')
		if 'gratuitos' in session:
			gratuitos=session['gratuitos']
		else:
			gratuitos=get_freechampions(apikey,region)
		lista=[gratuitos,0]
	elif request.method == 'POST':
		session.pop('perfil',None)
		nombre =request.form.get('nombre')
		region =request.form.get('region')
		if 'region' in session and region!=session['region']:
			session.pop('gratuitos',None)
			#save_champions(apikey,region)
			#save_spells(apikey)
		plantilla,lista=get_fullinfo(apikey,nombre,region)
		if lista[1]!=1:
			session['perfil']=lista
			session['region']=region
	return render_template(plantilla,lista=lista)

@app.route('/perfil')
def perfil():
	if 'perfil' in session:
		lista=session['perfil']
		return render_template('perfil.html',lista=lista)
	else:
		return redirect('/')

@app.route('/historial')
def historial():
	if session:
		lista=session['historial']
		return render_template('historial.html',lista=lista)
	else:
		return redirect('/')

@app.route('/maestrias')
def maestrias():
	if request.method == 'GET':
		return render_template('maestrias.html')


@app.route('/jugador/<nombre>')
def jugadores(nombre):
	region = session['region']
	plantilla,lista=get_fullinfo(apikey,nombre,region)
	session['perfil']=lista
	return render_template(plantilla,lista=lista)




app.run('0.0.0.0',int(port), debug=True)

