import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DB_HOST = config['DATABASE']['DB_HOST']
DB_PORT = int(config['DATABASE']['DB_PORT'])
API_KEY = config['API']['API_KEY']

def connect_db():
    print(f"Connecting to {DB_HOST}: {DB_PORT}...")
    # db connection logic here

def call_api():
    print(f"Calling API with key: {API_KEY}...")
    # api call logic here

if __name__ == "__main__":
    connect_db()
    call_api()