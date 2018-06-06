import requests

version='8.11.1'
## realización de requests general
def get_requests(apikey,url):
	cabecera={"api_key":apikey}
	r1=requests.get(url,params=cabecera)
	if r1.status_code == 200:
		return r1.json()
	else:
		return {}

## obtener version actual del juego
def get_version(apikey,region):
	url='https://'+region+'.api.riotgames.com/lol/static-data/v3/versions'
	doc_req=get_requests(apikey,url)
	return doc_req[0]


## informacion jugador
def get_info(apikey,nombre,region):
	url='https://'+region+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+nombre
	doc_req=get_requests(apikey,url)
	if doc_req:
		#version=get_version(apikey,region)
		doc_req['icono']='http://ddragon.leagueoflegends.com/cdn/'+version+'/img/profileicon/'+str(doc_req['profileIconId'])+'.png'
		return doc_req
	else:
		return {}

## partida actual
def get_actual(apikey,idinvocador,region):
	url='https://'+region+'.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/'+str(idinvocador)
	doc_req=get_requests(apikey,url)
	return doc_req


## posicion rankeds
def get_liga(apikey,idinvocador,region):
	url='https://'+region+'.api.riotgames.com/lol/eague/v3/positions/by-summoner/'+str(idinvocador)
	doc_req=get_requests(apikey,url)
	return doc_req

#	tipo=res['queueType']
#	nombreliga=res['leagueName']
#	nivel1=res['tier']
#	nivel2=res['rank']
#	puntos=res['leaguePoints']
#	partidasganadas=res['wins']
#	partidasperdidas=res['losses']