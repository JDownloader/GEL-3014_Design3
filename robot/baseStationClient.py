import requests
import constants as cte
import json


class BaseStationClient():
    def __init__(self, application):
        self.app = application

    def fetch_flag(self):
        response = requests.get(self.app.base_station_ip_address + cte.FLAG_RESSOURCE)
        return json.loads(response.text)['flag']

    def fetch_robot_position(self):
        response = requests.get(self.app.base_station_ip_address + cte.ROBOT_POSITION_RESSOURCE)
        return json.loads(response.text)['position']
