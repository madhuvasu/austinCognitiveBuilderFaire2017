import os
import json
import sys
import requests

from smartystreets import Client
from flask import Flask, jsonify, request, send_from_directory, Response
from watson_developer_cloud import ToneAnalyzerV3, VisualRecognitionV3, LanguageTranslatorV2

#tone_analyser = ToneAnalyzerV3(username='9a6fe37b-d509-4eb1-bac7-5f9d5fc52e32', password='MFDIpx6y5Acc', version='2017-05-19')
#tone = tone_analyser.tone("Is this sentence funny or not!??!")
#print(tone)


app = Flask(__name__)

#Building a webserver or web page. / is the homepage for our server, we are printing hello world on it
@app.route('/', methods=['GET'])
def home():
	path = os.path.abspath(os.path.dirname(__file__))
	src = os.path.join(path, 'index.html')
	content = open(src).read()
    	return Response(content, mimetype="text/html")

@app.route('/version')
def version():
	return sys.version

@app.route('/power/<int:base>/<int:exponent>')
def power(base, exponent):
	return str(base ** exponent)

@app.route('/tone/<text>')
def tone(text):
	tone_analyser = ToneAnalyzerV3(username='764d55b0-ca85-4bb4-9ff9-9e4b0161d681', password='KEOzscgHHsCC', version='2017-05-19')
	tone = tone_analyser.tone(text)
	return jsonify(tone)

def numberOfCrimeInstances(jasonCrimeData, inputZipCode):
	client = Client('8f68685d-6655-4fa5-a831-23aa3fcab8ea', 'hNjDuE332bBR3dkwYTxW')
	zipCodeJasonCrimeData = []
	for item in jasonCrimeData:
                address = str(item.get('address')) + ", Austin, Texas"
		address = address.upper().replace(' BLOCK', '')
		crimeType = str(item.get('crime_type'))
		properAddress = client.street_address(address)
		if properAddress != None:
			zipCode = str(properAddress['components']['zipcode'])
 	        	#from IPython import embed
        		#embed()
			zipCodeJasonCrimeData.append(zipCode)
	return zipCodeJasonCrimeData.count(str(inputZipCode))

@app.route('/crimedata/<int:inputZipCode>')
def crimedata(inputZipCode):
	url = "https://data.austintexas.gov/resource/e6ir-dgdv.json"
	response = requests.get(url)
	#from IPython import embed
	#embed()
	jasonCrimeData = (response.json())
	return str(numberOfCrimeInstances(jasonCrimeData, inputZipCode))
	#return jsonify(response.json())

#Boiler plate code for this thing to start

if __name__ == '__main__':
	#look for the envt variable PORT, if not defined, define it to 9099
	port = int(os.getenv('PORT', 9090))
	# run your application and listen at 0.0... which is the local ip address, at port 9099
	app.run(host='0.0.0.0', port=port)
	
