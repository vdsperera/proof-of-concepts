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

config = Config('config.json')
DB_HOST = config.db_host
DB_PORT = int(config.db_port)
API_KEY = config.api_key

def connect_db():
    print(f"Connecting to {DB_HOST}: {DB_PORT}...")
    # db connection logic here

def call_api():
    print(f"Calling API with key: {config.api_key}...")
    # api call logic here

if __name__ == "__main__":
    connect_db()
    call_api()