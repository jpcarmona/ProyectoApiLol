from flask import Flask, url_for,render_template,request,abort
import requests

def get_requests(key,url):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	if r1.status_code == 200:
		doc = r1.json()
		return doc


@app.route("/")
def inicio():
	doc = etree.parse('museos.xml')
	museos=doc.xpath('//SimpleData[@name="NOMBRE"]/text()')
	ids=doc.xpath('//SimpleData[@name="FID"]/text()')
	datos=zip(ids,museos)
	return render_template("inicio.html",datos=datos)