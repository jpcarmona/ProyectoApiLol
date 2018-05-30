from flask import Flask, url_for,render_template,request,abort
import requests

app = Flask(__name__)

port = 5000

@app.route('/')
def inicio():
	return render_template('index.html')

def get_requests(key,url):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	if r1.status_code == 200:
		doc = r1.json()
		return doc


app.run('0.0.0.0',int(port), debug=True)