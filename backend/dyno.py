import boto3
import requests

city = "Dubai"
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('weather-app-city-list')

db.put_item(
			Item={
				'city': city,
			}
)

res = db.scan(
	Select='ALL_ATTRIBUTES'
)
print('res.items')
for element in res['Items']:
	print(element['city'])

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

print(weather_data)

