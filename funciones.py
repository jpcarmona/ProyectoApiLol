import requests,json

#version='8.11.1'
## realización de requests general
def get_requests(apikey,url):
	cabecera={"api_key":apikey}
	r1=requests.get(url,params=cabecera)
	if r1.status_code == 200:
		return r1.json()
	else:
		return {}

## obtener version actual del juego
#def get_version(apikey,region):
#    url='https://'+region+'.api.riotgames.com/lol/static-data/v3/versions'
#    doc_req=get_requests(apikey,url)
#    return doc_req[0]

def get_version():
	with open('version.json', 'r') as fichero:
		datos = json.load(fichero)
	return datos['version']

## obtener apikey
def get_apikey():
	with open('apikey.json', 'r') as fichero:
		datos = json.load(fichero)
	return datos['apikey']

## informacion jugador
def get_info(apikey,nombre,region): 
	url='https://'+region+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+nombre
	doc_req=get_requests(apikey,url)
	if doc_req:
		version=get_version()
		doc_req['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/profileicon/'+str(doc_req['profileIconId'])+'.png'
	return doc_req

## obtener todos los campeones
def get_champions(apikey):
	region='euw1'
	version=get_version()
	url='https://'+region+'.api.riotgames.com/lol/static-data/v3/champions?locale=es_ES&version='+version+'&dataById=true'
	doc_req=get_requests(apikey,url)
	return doc_req['data']

## guardar campeones en fichero
def save_champions(apikey):
	doc_champions=get_champions(apikey)
	doc_req={}
	with open('campeones.json', 'w') as fichero:
		for key,value in doc_champions.items():
			doc_req[key]=value['name']
		json.dump(doc_req, fichero)

## obtener campeon
#def get_champion(apikey,id,region):
#   version=get_version()
#    url='https://'+region+'.api.riotgames.com/lol/static-data/v3/champions/'+str(id)+'?locale=es_ES&version='+version
#    doc_req=get_requests(apikey,url)
#    nombre=doc_req['name']
#    doc_req['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/champion/'+nombre+'.png'
#    return doc_req

def get_champion(id):
	with open('campeones.json', 'r') as fichero:
		campeones = json.load(fichero)
	campeon=campeones[str(id)]
	return campeon

## posicion rankeds
def get_liga(apikey,idinvocador,region):
	doc_req={}
	url='https://'+region+'.api.riotgames.com/lol/league/v3/positions/by-summoner/'+str(idinvocador)
	doc=get_requests(apikey,url)
	for i in doc:
		if i['queueType']=="RANKED_SOLO_5x5":
			doc_req['ganadas']=i['wins']
			doc_req['perdidas']=i['losses']
			doc_req['posicion']=i['rank']
			doc_req['liga']=i['tier']
			doc_req['puntos']=i['leaguePoints']
	return doc_req

## maestria con campeon
def get_mastery_champion(apikey,idinvocador,region):
	url='https://'+region+'.api.riotgames.com/lol/eague/v3/positions/by-summoner/'+str(idinvocador)
	doc_req=get_requests(apikey,url)
	return doc_req

## partida actual
def get_actual(apikey,idinvocador,region):
	url='https://'+region+'.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/'+str(idinvocador)
	doc_req=get_requests(apikey,url)
	return doc_req

def partida_actual(partida,apikey,region):
	#version=get_version(apikey,region)
	doc_req={}
	version=get_version()
	doc_req['equipo1']={}
	doc_req['equipo2']={}
	for jugador in partida:
		invocador={}        
		invocador['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/profileicon/'+str(jugador['profileIconId'])+'.png'
		invocador['campeon']=get_champion(jugador['championId'])
		invocador['nombre']=jugador['summonerName']
		invocador['liga']=get_liga(apikey,jugador['summonerId'],region)
		n1=1
		n2=1
		if jugador['teamId']==100:			
			doc_req['equipo1']['jugador'+str(n1)]=invocador
			n1+=1
		elif jugador['teamId']==200:			
			doc_req['equipo2']['jugador'+str(n2)]=invocador
			n2+=1
	return doc_req



