
from flowthings import API, Token 
from flask import Flask, request, jsonify
import time 


app = Flask(__name__)

token = 'l2VuxNAeUuNnQcncNSL8vUjckYcH7Kyu'
account = 'prateek91'
flow_path = '/stamford2016/hack-data/by-location/sic/wad/ms6'


ms6 = 'f56c4c83d68056d7a7d420452'
pg6 = 'f56c4c82b68056d7a7d420412'
ps6 = 'f56c4c82768056d7a7d420405'

creds = Token(account, token)
api  = API(creds)


@app.route('/getMS')
def msData():
	data = api.drop(ms6).find()
	return jsonify({"data":data})


if __name__ =="__main__":
	app.debug =True
	app.run('0.0.0.0', port =8080)
