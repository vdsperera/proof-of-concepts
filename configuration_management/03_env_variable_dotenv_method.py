from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
API_KEY = os.getenv("API_KEY")


def connect_db():
    print(f"Connecting to {DB_HOST}:{DB_PORT}...")
    # db connection logic here

def call_api():
    print(f"Calling API with key: {API_KEY}...")
    # api call logic here

if __name__ == "__main__":
    connect_db()
    call_api()