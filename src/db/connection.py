from sqlalchemy import create_engine, Connection
import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, connect_args={'options': '-csearch_path=jobs,public'})

def get_connection() -> Connection:
    return engine.connect()