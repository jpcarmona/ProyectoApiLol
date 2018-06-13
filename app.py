from flask import Flask, redirect, render_template, request, session
from funciones import *
import os

app = Flask(__name__)
app.secret_key=str(os.system('openssl rand -base64 24'))

port = os.environ['PORT']
apikey=get_apikey()
#act_docs(apikey) ## actualizar ficheros (consume mucho a la api)


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
			session['gratuitos']=gratuitos
		lista=[gratuitos]
	elif request.method == 'POST':
		session.pop('perfil',None)
		session.pop('lista',None)
		session.pop('partidas',None)
		nombre =request.form.get('nombre')
		region =request.form.get('region')
		if 'region' in session and region!=session['region']:
			session.pop('gratuitos',None)
			#act_docs(apikey,region)
		plantilla,lista=get_fullinfo(apikey,nombre,region)		
		session['region']=region
		if lista[0]!=1:
			session['lista']=lista
			session['perfil']=lista[0]
		else:
			gratuitos=get_freechampions(apikey,region)
			lista=[gratuitos,1]
	return render_template(plantilla,lista=lista)

@app.route('/perfil')
def perfil():
	if 'lista' in session:
		lista=session['lista']
		return render_template('perfil.html',lista=lista)
	else:
		return redirect('/')

@app.route('/jugador/<nombre>')
def jugadores(nombre):
	region = session['region']
	plantilla,lista=get_fullinfo(apikey,nombre,region)
	session['perfil']=lista
	return render_template(plantilla,lista=lista)

@app.route('/historial',methods=['POST','GET'])
def historial():
	if 'perfil' in session:
		if request.method == 'POST':
			valor=request.form.get('valor')
			if valor=='Mostrar todo el historial':
				return redirect('/historial/1')
			elif valor=='Buscar':
				campeon=request.form.get('campeon')
				return redirect('/historial/campeon/'+campeon)
			elif valor=='Victorias':
				return redirect('/historial/partidas/ganadas')
			elif valor=='Buscar':
				return redirect('/historial/partidas/perdidas')
		else:
			return render_template('historial.html',partidas=[])
	else:
		return redirect('/')

@app.route('/historial/<pagina>')
def paginas(pagina):
	pagina=int(pagina)
	region = session['region']
	idcuenta=session['perfil']['accountId']
	lista=session['perfil']
	partidas,total=get_historial(apikey,idcuenta,region,pagina)
	return render_template('historial.html',partidas=partidas,lista=lista,pagina=pagina,total=total)

@app.route('/maestrias')
def maestrias():
	if request.method == 'GET':
		return render_template('maestrias.html')


app.run('0.0.0.0',int(port), debug=True)

