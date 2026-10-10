from clients.base_client import BaseClient

class MainpageClient(BaseClient):

    def get_mainpage(self):
        return self.get(f'/')

    def get_currencies(self):
        return self.get(f'/api/currency')