import requests
from flask import render_template
from flask_restful import Resource, reqparse

API_KEY = '0eb7686230adc4476c78be6a9a308703'

class CityWeatherController(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city_name', type=str)
        args = parser.parse_args()
        try:
            city_name = args['city_name']
            if not city_name:
                raise NameError
        except:
            return {'status': 'error',
                    'data': 'Invalid city name'}, 400
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}' \
            .format(args['city_name'], API_KEY)
        response = requests.get(url)
        try:
            if response.status_code == 200 and response.json():
                resp_json = response.json()
                city = resp_json['name']
                country_code = resp_json['sys']['country']
                details = resp_json['weather'][0]['description'].capitalize()
                icon_url = 'http://openweathermap.org/img/w/{}.png'.format(resp_json['weather'][0]['icon'])
                avg_temp = resp_json['main']['temp']
                min_temp = resp_json['main']['temp_min']
                max_temp = resp_json['main']['temp_max']
                humidity = resp_json['main']['humidity']
                wind = resp_json['wind']['speed']
            else:
                return {'status': 'error',
                        'data': 'City not found'}, 404
        except:
            return {'status': 'error',
                    'data': 'Invalid response from OpenWeatherMap'}, 500
        return {'status': 'success',
                'data': render_template('components/weather_table.html',
                                        city=city,
                                        country_code=country_code,
                                        weather_details=details,
                                        icon_url=icon_url,
                                        avg_temp=avg_temp,
                                        min_temp=min_temp,
                                        max_temp=max_temp,
                                        humidity=humidity,
                                        wind=wind)}