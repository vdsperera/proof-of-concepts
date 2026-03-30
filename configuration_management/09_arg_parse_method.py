import argparse
import configparser

parser = argparse.ArgumentParser()
parser.add_argument('--db_url', help='Override the database URL')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')

DB_HOST = args.db_url if args.db_url else config['DATABASE']['DB_HOST']

def connect_db():
    print(f"Connecting to {DB_HOST}...")
    # db connection logic here

if __name__ == "__main__":
    connect_db()