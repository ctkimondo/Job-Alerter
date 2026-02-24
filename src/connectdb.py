import os
from dotenv import load_dotenv
import psycopg2 # This library enables python to talk to Postgres

# Finds the .env file and loads contents to memory
load_dotenv()

# Fetch the secrets from memory
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host="localhost", # Talks to docker port
            port="5433",
            database=db_name,
            user=db_user,
            password=db_password
        )
        print("Successfully connected to the database")
        return connection
    except Exception as e:
        print(f"Connection failed: {e}")




