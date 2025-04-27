import os
from databases import Database
from dotenv import load_dotenv

load_dotenv()

SYSTEM_DATABASE_URL = os.getenv("SYSTEM_DATABASE_URL")
CLIENT_DATABASE_URL = os.getenv("CLIENT_DATABASE_URL")

system_database = Database(SYSTEM_DATABASE_URL)
client_database = Database(CLIENT_DATABASE_URL)
