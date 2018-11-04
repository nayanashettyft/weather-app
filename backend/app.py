import requests
from flask import Flask, jsonify, request, logging
import boto3
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=['http://weather-report-app.s3-website-eu-west-1.amazonaws.com'])

dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('weather-app-city-list')

@app.route('/weather', methods=['GET', 'POST'])
def weather_report():
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
	if request.method == 'POST':
		city = request.args.get('city')
		print(city)

		# db.put_item(
		# 	Item={
		# 		'city': city,
		# 	}
		# )
		# print("Written data into dynamoDB")
		# r = requests.get(url.format(city)).json()
		# weather = {
		# 	'city' : city,
		# 	'temperature' : r['main']['temp'],
		# 	'description' : r['weather'][0]['description'],
		# 	'icon' : r['weather'][0]['icon'],
		# }
		return jsonify({'status': 'added'})
	
	res = db.scan(
		Select='ALL_ATTRIBUTES'
	)

	weather_data = []

	for element in res['Items']:
		city = element['city']
		r = requests.get(url.format(city)).json()
		weather = {
			'city' : city,
			'temperature' : r['main']['temp'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}
		weather_data.append(weather)

	#print(weather_data)

	return jsonify({'weather': weather_data})


@app.route('/weather/add', methods=['POST'])
def weather_add_report():
	city = request.args.get("city", "")
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
	#args = request.args.to_dict()
	#city = request.args.get('city')
	#print(args)

		# db.put_item(
		# 	Item={
		# 		'city': city,
		# 	}
		# )
		# print("Written data into dynamoDB")
		# r = requests.get(url.format(city)).json()
		# weather = {
		# 	'city' : city,
		# 	'temperature' : r['main']['temp'],
		# 	'description' : r['weather'][0]['description'],
		# 	'icon' : r['weather'][0]['icon'],
		# }
	return jsonify({'status': city})

