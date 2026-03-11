from sqlalchemy import create_engine, text

import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
with open("db/schema.sql") as f:
    sql = f.read()
    print(sql)

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()