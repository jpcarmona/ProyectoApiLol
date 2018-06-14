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
#def get_apikey():
#	with open('docs/apikey.json', 'r') as fichero:
#		datos = json.load(fichero)
#	return datos['apikey']

## obtener fecha
def get_fecha(milisegundos):
	segundos=(milisegundos/1000) -180 ## retraso de partida
	fecha=datetime.datetime.fromtimestamp(segundos).strftime('%Y-%m-%d %H:%M:%S')
	return fecha

## obtener tiempo partida
def get_tiempo(milisegundos):
	segundos=(milisegundos/1000)
	tiempo=datetime.datetime.now()-datetime.datetime.fromtimestamp(segundos)
	minutos=int(tiempo.seconds/60)
	return str(minutos)

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

## obtener ID campeon sin llamar a la api
def get_idchampion(campeon):
	idcampeon=''
	with open('docs/campeones.json', 'r') as fichero:
		campeones = json.load(fichero)
	for key,value in campeones.items():
		if value['imagen'].lower()==campeon.lower():
			idcampeon=key
	return idcampeon

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
	try:
		spell='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/spell/'+spells[str(id)]['imagen']
	except:
		spell=''	
	return spell

## obtener todos los objetos
def get_objetos(apikey,region):
	version=get_version()
	url='https://'+region+'.api.riotgames.com/lol/static-data/v3/items?locale=es_ES&itemListData=image&version='+version+'&tags=image'
	doc_req=get_requests(apikey,url)
	return doc_req['data']

## guardar objetos en fichero
def save_objetos(apikey,region):
	doc_objetos=get_objetos(apikey,region)
	doc_req={}
	with open('docs/objetos.json', 'w') as fichero:
		doc_req['0']={}
		doc_req['0']['imagen']=''
		for key,value in doc_objetos.items():
			doc_req[key]={}
			doc_req[key]['imagen']=value['image']['full']
		json.dump(doc_req, fichero)

## obtener objeto sin llamar a la api
def get_objeto(id):
	version=get_version()
	with open('docs/objetos.json', 'r') as fichero:
		objetos = json.load(fichero)
	try:
		objeto='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/item/'+objetos[str(id)]['imagen']
	except:
		objeto=''
	return objeto

## actualizar ficheros docs
def act_docs(apikey,region=''):
	if not region:
		region='euw1' ## region por defecto
	save_champions(apikey,region)
	save_spells(apikey,region)
	save_objetos(apikey,region)

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

## obtiene la partida personalizada
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

## obtiene la lista
def get_fullinfo(apikey,nombre,region):
	version=get_version()
	doc_info =get_info(apikey,nombre,region)
	if doc_info:
		plantilla =('perfil.html')
		doc_info['liga']=get_liga(apikey,doc_info['id'],region)
		doc_actual =get_actual(apikey,doc_info['id'],region)		
		partida={}		
		if doc_actual:
			partida =partida_actual(doc_actual['participants'],apikey,region)
			partida['tiempo']=get_tiempo(doc_actual['gameStartTime'])
			partida['mapa']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/map/map'+str(doc_actual['mapId'])+'.png'
		lista=[doc_info,doc_actual,partida]
	else:
		plantilla =('index.html')
		lista=[1]
	return plantilla,lista

## obtiene la partida
def get_partida(apikey,idpartida,region):
	url='https://'+region+'.api.riotgames.com/lol/match/v3/matches/'+str(idpartida)
	doc_req=get_requests(apikey,url)
	return doc_req

## obtiene datos simples de partida
def get_partidasimple(partida,idcuenta):
	version=get_version()
	for equipo in partida['teams']:
		if equipo['win']=='Win':
			equipoganador=equipo['teamId']
	doc_req={}
	doc_req['modo']=partida['gameMode']
	doc_req['mapa']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/map/map'+str(partida['mapId'])+'.png'
	doc_req['tiempo']=int(partida['gameDuration']/60)
	doc_req['jugador']={}
	for jugador in partida['participantIdentities']:
		if jugador['player']['accountId']==idcuenta:
			idjugador=jugador['participantId']
	for jugador in partida['participants']:
		if jugador['participantId']==idjugador:
			doc_req['jugador']['spell1']=get_spell(jugador['spell1Id'])
			doc_req['jugador']['spell2']=get_spell(jugador['spell2Id'])
			doc_req['jugador']['item0']=get_objeto(jugador['stats']['item0'])
			doc_req['jugador']['item1']=get_objeto(jugador['stats']['item1'])
			doc_req['jugador']['item2']=get_objeto(jugador['stats']['item2'])
			doc_req['jugador']['item3']=get_objeto(jugador['stats']['item3'])
			doc_req['jugador']['item4']=get_objeto(jugador['stats']['item4'])
			doc_req['jugador']['item5']=get_objeto(jugador['stats']['item5'])
			doc_req['jugador']['item6']=get_objeto(jugador['stats']['item6'])
			doc_req['jugador']['kills']=jugador['stats']['kills']
			doc_req['jugador']['assists']=jugador['stats']['assists']
			doc_req['jugador']['deaths']=jugador['stats']['deaths']
			doc_req['jugador']['minions']=jugador['stats']['totalMinionsKilled']
			doc_req['jugador']['oro']=jugador['stats']['goldEarned']
			if jugador['teamId']==equipoganador:
				doc_req['jugador']['gana']=True
			else:
				doc_req['jugador']['gana']=False
	return doc_req

## obtiene el historial
def get_historial(apikey,idcuenta,region,pagina,tipo=''):
	end=pagina*10
	begin=end-10
	idcampeon=get_idchampion(tipo)
	if tipo !='todo':
		url='https://'+region+'.api.riotgames.com/lol/match/v3/matchlists/by-account/'+str(idcuenta)+'?beginIndex='+str(begin)+'&champion='+str(idcampeon)+'&endIndex='+str(end)		
	else:
		url='https://'+region+'.api.riotgames.com/lol/match/v3/matchlists/by-account/'+str(idcuenta)+'?beginIndex='+str(begin)+'&endIndex='+str(end)
	doc=get_requests(apikey,url)
	doc_req=[]
	total=doc['totalGames']
	for partida in doc['matches']:
		idpartida=partida['gameId']
		version=get_version()
		campeon=get_champion(partida['champion'])
		campeon['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/champion/'+campeon['imagen']+'.png'
		fecha=get_fecha(partida['timestamp'])
		partida=get_partida(apikey,idpartida,region)
		partidasimple=get_partidasimple(partida,idcuenta)
		doc_req.append({'idpartida':idpartida,'campeon':campeon,'fecha':fecha,'partidasimple':partidasimple})
	return doc_req,total,idcampeon

## maestria con campeon
#def get_mastery_champion(apikey,idinvocador,region):
#	url='https://'+region+'.api.riotgames.com/lol/eague/v3/positions/by-summoner/'+str(idinvocador)
#	doc_req=get_requests(apikey,url)
#	return doc_req
