import requests

class BaseClient:
    def __init__(self, base_url):
        self.url = base_url

    def get(self, endpoint, **kwargs):
        return requests.get(self.url + endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return requests.post(self.url + endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return requests.delete(self.url + endpoint, **kwargs)

