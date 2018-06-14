from flask import Flask, redirect, render_template, request, session
from funciones import *
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
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
	session['lista']=lista
	session['perfil']=lista[0]
	return render_template(plantilla,lista=lista)

@app.route('/historial',methods=['POST','GET'])
def historial():
	if 'perfil' in session:
		if request.method == 'POST':
			valor=request.form.get('valor')
			if valor=='Mostrar todo el historial':
				return redirect('/historial/todo/1')
			elif valor=='Buscar':
				campeon=request.form.get('campeon')
				return redirect('/historial/'+campeon+'/1')
			elif valor=='Victorias':
				return redirect('/historial/ganadas/1')
			elif valor=='Buscar':
				return redirect('/historial/perdidas/1')
		else:
			return render_template('historial.html',partidas=[],pagina='')
	else:
		return redirect('/')

@app.route('/historial/<tipo>/<pagina>')
def paginas_tipo(pagina,tipo):
	pagina=int(pagina)
	region = session['region']
	idcuenta=session['perfil']['accountId']
	lista=session['perfil']
	partidas,total,idcampeon=get_historial(apikey,idcuenta,region,pagina,tipo)
	return render_template('historial.html',partidas=partidas,lista=lista,pagina=pagina,total=total,tipo=tipo,idcampeon=idcampeon)

@app.route('/maestrias')
def maestrias():
	if request.method == 'GET':
		return render_template('maestrias.html')

## twitter


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
CONSUMER_KEY = 'HlAti771ujp4EQImR5D78RZY1'
CONSUMER_SECRET = '4Nwzprz3C3UlOHTjoms1UJW4SA2ghiGxOvpe4JMaK2XBYDBftV'
update_url = 'https://api.twitter.com/1.1/statuses/update.json'

def get_request_token_oauth1():
	oauth = OAuth1(CONSUMER_KEY,
				client_secret=CONSUMER_SECRET)
	r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
	credentials = parse_qs(r.content)
	return credentials.get(b'oauth_token')[0]

def get_access_token_oauth1(request_token,verifier):
	oauth = OAuth1(CONSUMER_KEY,
					client_secret=CONSUMER_SECRET,
					resource_owner_key=request_token,
					verifier=verifier,)
	r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
	credentials = parse_qs(r.content)
	session["screen_name"] = credentials.get(b'screen_name')[0]
	return credentials.get(b'oauth_token')[0],credentials.get(b'oauth_token_secret')[0]

@app.route('/twitter')
def twitter():
	request_token = get_request_token_oauth1()
	authorize_url = AUTHENTICATE_URL + request_token.decode("utf-8")
	session["request_token"]=request_token.decode("utf-8")
	return redirect(authorize_url)

@app.route('/callback', methods=["GET", "POST"])
def callback():
	request_token=session["request_token"]
	verifier  = request.args.get("oauth_verifier")
	access_token,access_token_secret= get_access_token_oauth1(request_token,verifier)
	session["access_token"]= access_token.decode("utf-8")
	session["access_token_secret"]= access_token_secret.decode("utf-8")
	return """<html><head></head><body>
	<form method="POST" action="/twittear">
	<input name="status_update" type="text" value="hello"/>
	<input type="submit" value="Send"/>
	</form></body></html>"""

@app.route('/twittear', methods=["POST"])
def twittear():
	update = request.form["status_update"]
	post = {"status": update}
	access_token=session["access_token"]
	access_token_secret=session["access_token_secret"]
	oauth = OAuth1(CONSUMER_KEY,
				client_secret=CONSUMER_SECRET,
				resource_owner_key=access_token,
				resource_owner_secret=access_token_secret)
	url = update_url
	r=requests.post(url, data=post, auth=oauth)
	if r.status_code==200:
		return redirect("https://twitter.com/#!/%s" % session["screen_name"])

app.run('0.0.0.0',int(port), debug=True)

