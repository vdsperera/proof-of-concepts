from decouple import config

DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT', cast=int)
API_KEY = config('API_KEY')

def connect_db():
    print(f"Connecting to {DB_HOST}:{DB_PORT}...")
    # db connection logic here

def call_api():
    print(f"Calling API with key: {API_KEY}...")
    # api call logic here

if __name__ == "__main__":
    connect_db()
    call_api()
