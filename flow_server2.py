
from flowthings import API, Token,mem
from flask import Flask, request, jsonify
from datetime import datetime
import time, numpy 

SERIES_LIMIT = 100
THRESHOLD_TEMP_UP = 27
THRESHOLD_TEMP_DOWN=25


# Flowthings
token = 'l2VuxNAeUuNnQcncNSL8vUjckYcH7Kyu'
account = 'prateek91'
flow_path = '/stamford2016/hack-data/by-location/sic/wad/ms6'


ms6 = 'f56c4c83d68056d7a7d420452'
pg6 = 'f56c4c82b68056d7a7d420412'
ps6 = 'f56c4c82768056d7a7d420405'

creds = Token(account, token)
api  = API(creds)

ALERT_ON = 0

# yelp
import argparse
import json
import pprint
import sys
import urllib
import urllib2

import oauth2

from yelp import search


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

CONSUMER_KEY = '4TR4fqGYHAqNwtm53qmDfA'
CONSUMER_SECRET = 't9fDu1LhppKfXbyI4FQQjctR6q4'
TOKEN = '78kXtgCIHcg02ZCGJ9EGNLEZdJWTvxFh'
TOKEN_SECRET = 'wwmnyh8ZBjgM6AKp0S16WHt4smk'

app = Flask(__name__)

@app.route('/getMS')
def msData():
	data = api.drop(ms6).find()
	return jsonify({"data":data})


@app.route('/getTemperatureData')
def tempData():
	temperature_data = api.drop(ms6).find(mem.elems.temperature_degcc_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	new = 0
	for i in temperature_data:
		value = i['elems']['temperature_degcc_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['temperature_degcc_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		if new != time:
			tmp_data.append({'value':value, 'time':time})
			new = time

	return jsonify({'series': tmp_data})

@app.route('/getLightData')
def lightData():
	luminescence_data = api.drop(ms6).find(mem.elems.luminiscence_lux_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	new = 0
	for i in luminescence_data:
		value = i['elems']['luminiscence_lux_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['luminiscence_lux_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')	
		if new != time:
			tmp_data.append({'value':value, 'time':time})
			new = time
	return jsonify({'series': tmp_data})

@app.route('/getMotionData')
def motionData():
	motion_data = api.drop(ms6).find(mem.elems.alarm_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	new = 0
	for i in motion_data:
		value = i['elems']['alarm_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['alarm_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		if new != time:
			tmp_data.append({'value':value, 'time':time})
			new = time

	return jsonify({'series': tmp_data})

@app.route('/getUvData')
def uvData():
	uv_data = api.drop(ms6).find(mem.elems.ultraviolet_uv_index_0.time > 0, limit=SERIES_LIMIT)
	tmp_data = []
	new  = 0	
	for i in uv_data:
		value = i['elems']['ultraviolet_uv_index_0']['value']['value']['value']
		time = datetime.fromtimestamp(i['elems']['ultraviolet_uv_index_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')		
		if new != time:
			tmp_data.append({'value':value, 'time':time})
			new = time

	return jsonify({'series': tmp_data})

@app.route('/getAlerts')
def getAlerts():
	alerts = []
	temp_alert = getTempAlert()
	if temp_alert:
		alerts.append(temp_alert)
	return jsonify({'alerts':alerts})

@app.route('/getFakeAlert')
def getFake():
	global ALERT_ON
	if ALERT_ON == 0:
		alerts2 =  [{ 'attribute':'temperature','alert': "High Temperature Alert. You might want to check on your baby.", "Trend": "Continuously Increasing"}]
	else: 
		alerts2 = []

	print ALERT_ON

	return  jsonify({'alerts': alerts2})

@app.route('/actionStatus', method = ['POST'])
def actionStatus():
	action = request.get_json()[u'action']
	print action
	global ALERT_ON

	if action == 1:
		ALERT_ON  = 1
	if action == 0:
		ALERT_ON = 0

	print  ALERT_ON
	return jsonify({'stauts':200})

@app.route('/getYelpSuggestions')
def getYelpSuggestions():
	params = request.get_json()
	term, location = params['term'], params['location']
	
	r = search(term, location)
	return jsonify(r)


def getTempAlert():
	x = api.drop(ms6).find(mem.elems.temperature_degcc_0.time > 0, limit=100)
	series, new = [],0
	for i in x:
		f = getTempData(i)
		if new != f['time']:
			series.append(f['value'])
			new = f['time']
		if len(series) > 20:
			break
	trend  = checkTrendAlert(series)

	if trend == 1:
		trend_str = "Continuously increasing"
	elif trend == -1:
		trend_str = "Continuously decreasing"
	else:
		trend_str = "normal"

	if trend == 1 and series[-1] > THRESHOLD_TEMP_UP:
		alert = "High Temperature Alert"
	elif trend == -1 and series[-1] < THRESHOLD_TEMP_DOWN:
		alert = "Low Temperature Alert"
	else:
		alert = "normal"
	
	if trend == 0 and alert == 'normal':
		return None
	return {'attribute': 'Temperature', "alert": alert, "trend":trend_str}

def checkTrendAlert(series):
	a,b = numpy.array(series), numpy.array([0] + series[1:])
	c = b-a
	if numpy.all(c < 0):
		return 1
	elif numpy.all(c<0):
		return -1
	return 0

def getTempData(i):
	value = i['elems']['temperature_degcc_0']['value']['value']['value']
	time = datetime.fromtimestamp(i['elems']['temperature_degcc_0']['value']['time']['value']).strftime('%Y-%m-%d %H:%M:%S')
	return {'value':value, 'time':time}





if __name__ =="__main__":
	app.debug =True
	app.run('0.0.0.0', port =8080)