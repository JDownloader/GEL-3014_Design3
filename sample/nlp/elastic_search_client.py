__author__ = 'Tea'

import requests

OK_STATUS_CODE = 200

class ElasticSearchClient :
    def __init__(self, url = "http://localhost:", port = "9200", index = "atlas"):
        self.url = url
        self.port = port
        self.index = index

    def post_request(self,query):
        url = self.url + self.port + "/" + self.index + "/" + "_search?pretty"
        response = requests.post(url, query)

        if response.status_code == OK_STATUS_CODE:
            return response.text
        else :
            return None

