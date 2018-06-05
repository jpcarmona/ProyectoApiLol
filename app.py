from flask import Flask, url_for, render_template, request, session
from funciones import *
import os

app = Flask(__name__)
port = os.environ['PORT']

apikey='RGAPI-037dca0f-a2a3-4901-86fe-d0a5941963d6'
region='euw1'

@app.route('/',methods=["post","get"])
def inicio():
	if request.method == "GET":
		return render_template('index.html')
	else:
		nombre = request.form.get("nombre")
		doc_info=get_info(apikey,nombre,region)
		return render_template('perfil.html',doc=doc_info)

#@app.route('/buscaperfil')
#def buscaperfil():
#	nombre = request.form.get("nombre")
#	payload={"api_key":apikey}
#	r=requests.get('https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+nombre,params=payload)
#	if r.status_code==200:
#		res=r.json()
#		nombreusuario=res['name']
#		profile=res['profileIconId']
#		level=res['summonerLevel']
#		idcuenta=res['accountId']
#		id1=res['id']
#		return render_template('perfil.html',nombre=nombreusuario,imagen=profile,nivel=level,idcuenta=idcuenta,id1=id1)

#@app.route('/perfil',methods=["post","get"])
#def perfil():
#	nombre = request.form.get("nombre")
#	payload={"api_key":apikey}
#	r=requests.get('https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+nombre,params=payload)
#	if r.status_code==200:
#		res=r.json()
#		nombreusuario=res['name']
#		profile=res['profileIconId']
#		level=res['summonerLevel']
#		idcuenta=res['accountId']
#		id1=res['id']
#		return render_template('perfil.html',nombre=nombreusuario,imagen=profile,nivel=level,idcuenta=idcuenta,id1=id1)







app.run('0.0.0.0',int(port), debug=True)
