# app.py
DB_HOST = "localhost"
DB_PORT = 5432
API_KEY = "my-secret-key"

def connect_db():
    print(f"Connecting to {DB_HOST}:{DB_PORT}...")
    # db connection logic here

def call_api():
    print(f"Calling API with key: {API_KEY}...")
    # api call logic here

if __name__ == "__main__":
    connect_db()
    call_api()