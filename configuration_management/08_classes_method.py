import json

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    @property
    def db_host(self):
        return self.config['DATABASE']['DB_HOST']

    @property
    def db_port(self):
        return int(self.config['DATABASE']['DB_PORT'])

    @property
    def api_key(self):
        return self.config['API']['API_KEY']