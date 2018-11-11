import requests
from flask import Flask, jsonify, request, logging
import boto3
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=['http://weather-report-app.s3-website-eu-west-1.amazonaws.com'])

dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('weather-app-city-list')

@app.route('/weather', methods=['GET', 'POST'])
def weather_report():
	if request.method == 'POST':
		data = request.data
		dataDict = json.loads(data.decode("utf-8").replace("'",'"'))
		city = dataDict['city']
		try:
			response = db.get_item(
				Key={
					'city':city
				}
			)
			item = response['Item']
			print("GetItem succeeded:")
			print(json.dumps(item, indent=4))
			return 0
		except KeyError as e:
			db.put_item(
				Item={
					'city': city,
				}
			)
			print("Written data into dynamoDB")
			return jsonify(weather_by_city(city))
	
	res = db.scan(
		Select='ALL_ATTRIBUTES'
	)
	weather_data = []
	for element in res['Items']:
		city = element['city']
		weather_data.append(weather_by_city(city))
	#print(weather_data)
	return jsonify(weather_data)


def weather_by_city(city):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
	r = requests.get(url.format(city)).json()
	temp_farenheit = r['main']['temp']
	temperature = (temp_farenheit - 32) * 5.0/9.0
	temp_celcius = round(temperature,2)
	weather = {
		'city' : city,
		'temperature' : temp_celcius,
		'description' : r['weather'][0]['description'],
		'icon' : r['weather'][0]['icon'],
	}
	return weather

