
from flowthings import API, Token,mem
from flask import Flask, request, jsonify
from datetime import datetime
import time 

SERIES_LIMIT = 20
token = 'l2VuxNAeUuNnQcncNSL8vUjckYcH7Kyu'
account = 'prateek91'
flow_path = '/stamford2016/hack-data/by-location/sic/wad/ms6'


ms6 = 'f56c4c83d68056d7a7d420452'
pg6 = 'f56c4c82b68056d7a7d420412'
ps6 = 'f56c4c82768056d7a7d420405'

creds = Token(account, token)
api  = API(creds)

app = Flask(__name__)

@app.route('/getMS')
def msData():
	data = api.drop(ms6).find()
	return jsonify({"data":data})


@app.route('/getTemperatureData')
def tempData():
	temperature_data = api.drop(ms6).find(mem.elems.temperature_degcc_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	for i in temperature_data:
		value = i['elems']['temperature_degcc_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['temperature_degcc_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		tmp_data.append({'value':value, 'time':time})

	return jsonify({'series': tmp_data})

@app.route('/getLightData')
def lightData():
	luminescence_data = api.drop(ms6).find(mem.elems.luminiscence_lux_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	for i in luminescence_data:
		value = i['elems']['luminiscence_lux_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['luminiscence_lux_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		tmp_data.append({'value':value, 'time':time})

	return jsonify({'series': tmp_data})

@app.route('/getMotionData')
def motionData():
	motion_data = api.drop(ms6).find(mem.elems.alarm_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	for i in motion_data:
		value = i['elems']['alarm_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['alarm_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		tmp_data.append({'value':value, 'time':time})

	return jsonify({'series': tmp_data})



@app.route('/getUvData')
def uvData():
	uv_data = api.drop(ms6).find(mem.elems.ultraviolet_uv_index_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	for i in uv_data:
		value = i['elems']['ultraviolet_uv_index_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['ultraviolet_uv_index_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		tmp_data.append({'value':value, 'time':time})

	return jsonify({'series': tmp_data})





if __name__ =="__main__":
	app.debug =True
	app.run('0.0.0.0', port =8080)