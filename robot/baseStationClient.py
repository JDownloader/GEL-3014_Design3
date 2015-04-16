import requests
import robotSrv.constants as cte
import json


class BaseStationClient():
    def __init__(self, application):
        self.app = application

    def fetch_flag(self):
        response = requests.get('http://' + self.app.base_station_ip_address + ':8000' + cte.FLAG_RESSOURCE)
        return json.loads(response.text)['flag']

    def fetch_robot_position(self):
        response = requests.get('http://' + self.app.base_station_ip_address + ':8000' + cte.ROBOT_POSITION_RESSOURCE)
        content = json.loads(response.text)
        return (content['angle'], content['position'])

    def fetch_cube_position(self, cube_color):
        data = {'color': cube_color}
        response = requests.post('http://' + self.app.base_station_ip_address + ':8000' + cte.CUBE_POSITION_RESSOURCE, data=data)
        content = json.loads(response.text)
        return (content['position_x'], content['position_y'])

    def send_pathfinding_itinerary(self, path):
        requests.post('http://' + self.app.base_station_ip_address + ':8000' + cte.PATH_RESSOURCE, data=str(path))
