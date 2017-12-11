import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import requests_cache
from flask import Flask
from flask_restful import Api

from weather_in_my_city.views import web_view
from weather_in_my_city.controllers.owm_controller import CityWeatherController

app = Flask(__name__, template_folder='templates', static_folder='static')
api = Api(app)
requests_cache.install_cache('wimc_cache', expire_after=600)

app.register_blueprint(web_view.bp)
api.add_resource(CityWeatherController, '/api/weather')

if __name__ == '__main__':
    print('running')
    app.run(port=5002)