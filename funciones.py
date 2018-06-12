import requests,json,datetime

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

## obtener version actual del juego sin llamar a la api
def get_version():
	with open('docs/version.json', 'r') as fichero:
		datos = json.load(fichero)
	return datos['version']

## obtener apikey
def get_apikey():
	with open('docs/apikey.json', 'r') as fichero:
		datos = json.load(fichero)
	return datos['apikey']

## obtener fecha
def get_fecha(milisegundos):
	segundos=(milisegundos/1000) -180 ## retraso de partida
	fecha=datetime.datetime.fromtimestamp(segundos).strftime('%Y-%m-%d %H:%M:%S')
	return fecha

## obtener tiempo partida
def get_tiempo(milisegundos):
	segundos=(milisegundos/1000) -180 ## retraso de partida
	tiempo=datetime.datetime.now()-datetime.datetime.fromtimestamp(segundos)
	minutos=int(tiempo.seconds/60)
	return minutos

## informacion jugador
def get_info(apikey,nombre,region): 
	url='https://'+region+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+nombre
	doc_req=get_requests(apikey,url)
	if doc_req:
		version=get_version()
		doc_req['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/profileicon/'+str(doc_req['profileIconId'])+'.png'
	return doc_req

## obtener todos los campeones
def get_champions(apikey,region):
	version=get_version()
	url='https://'+region+'.api.riotgames.com/lol/static-data/v3/champions?locale=es_ES&version='+version+'&champListData=image&tags=image&dataById=true'
	doc_req=get_requests(apikey,url)
	return doc_req['data']

## guardar campeones en fichero
def save_champions(apikey,region):
	doc_champions=get_champions(apikey,region)
	doc_req={}
	with open('docs/campeones.json', 'w') as fichero:
		for key,value in doc_champions.items():
			doc_req[key]={}
			doc_req[key]['nombre']=value['name']
			doc_req[key]['imagen']=value['key']
		json.dump(doc_req, fichero)

## obtener campeon
#def get_champion(apikey,id,region):
#   version=get_version()
#    url='https://'+region+'.api.riotgames.com/lol/static-data/v3/champions/'+str(id)+'?locale=es_ES&version='+version
#    doc_req=get_requests(apikey,url)
#    nombre=doc_req['name']
#    doc_req['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/champion/'+nombre+'.png'
#    return doc_req

## obtener campeon sin llamar a la api
def get_champion(id):
	with open('docs/campeones.json', 'r') as fichero:
		campeones = json.load(fichero)
	campeon=campeones[str(id)]
	return campeon

## campeones gratuitos
def get_freechampions(apikey,region):
	url='https://'+region+'.api.riotgames.com/lol/platform/v3/champions?freeToPlay=true'
	doc=get_requests(apikey,url)
	doc_req={}
	for champion in doc['champions']:
		campeon=get_champion(champion['id'])
		doc_req[campeon['nombre']]='http://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+campeon['imagen']+'_0.jpg'
	return doc_req

## obtener todos los spells
def get_spells(apikey,region):
	version=get_version()
	url='https://'+region+'.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=es_ES&version='+version+'&spellListData=image&dataById=true&tags=image'
	doc_req=get_requests(apikey,url)
	return doc_req['data']

## guardar spells en fichero
def save_spells(apikey,region):
	doc_spells=get_spells(apikey,region)
	doc_req={}
	with open('docs/spells.json', 'w') as fichero:
		for key,value in doc_spells.items():
			doc_req[key]={}
			doc_req[key]['imagen']=value['image']['full']
		json.dump(doc_req, fichero)

## obtener spell sin llamar a la api
def get_spell(id):
	version=get_version()
	with open('docs/spells.json', 'r') as fichero:
		spells = json.load(fichero)
	spell='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/spell/'+spells[str(id)]['imagen']
	return spell

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
	n1=1
	n2=1
	for jugador in partida:
		invocador={}
		campeon=get_champion(jugador['championId'])
		invocador['campeon']=campeon['nombre']
		invocador['icono']='http://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+campeon['imagen']+'_0.jpg'
		invocador['nombre']=jugador['summonerName']
		invocador['liga']=get_liga(apikey,jugador['summonerId'],region)
		invocador['spell1']=get_spell(jugador['spell1Id'])
		invocador['spell2']=get_spell(jugador['spell2Id'])
		if jugador['teamId']==100:
			doc_req['equipo1']['jugador'+str(n1)]=invocador
			n1+=1
		elif jugador['teamId']==200:
			doc_req['equipo2']['jugador'+str(n2)]=invocador
			n2+=1
	return doc_req

def get_fullinfo(apikey,nombre,region):
	doc_info =get_info(apikey,nombre,region)
	if doc_info:
		plantilla =('perfil.html')
		doc_info['liga']=get_liga(apikey,doc_info['id'],region)
		doc_actual =get_actual(apikey,doc_info['id'],region)		
		partida={}		
		if doc_actual:
			partida =partida_actual(doc_actual['participants'],apikey,region)
		partida['tiempo']=get_tiempo(doc_actual['gameStartTime'])
		lista=[doc_info,doc_actual,partida]
	else:
		plantilla =('index.html')
		region='euw1'
		gratuitos=get_freechampions(apikey,region)
		lista=[gratuitos,1]
	return plantilla,lista

## maestria con campeon
def get_mastery_champion(apikey,idinvocador,region):
	url='https://'+region+'.api.riotgames.com/lol/eague/v3/positions/by-summoner/'+str(idinvocador)
	doc_req=get_requests(apikey,url)
	return doc_req

#def get_historial():