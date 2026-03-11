from sqlalchemy import text, Connection
from src.db.connection import get_connection

import pandas as pd
def insert_company(conn: Connection, company: str):

    result = conn.execute(
        text("INSERT INTO companies (name) VALUES (:name) ON CONFLICT DO NOTHING RETURNING id"),
        {"name": company}
    )

    row = result.fetchone()

    if row:
        return row[0]

    result = conn.execute(
        text("SELECT id FROM companies WHERE name=:name"),
        {"name": company}
    )

    return result.fetchone()[0]

def insert_job(conn: Connection, title: str, description: str, company_id: str):

    conn.execute(
        text("""
        INSERT INTO jobs (title, description, company_id)
        VALUES (:title, :description, :company_id)
        """),
        {
            "title": title,
            "description": description,
            "company_id": company_id
        }
    )

def insert_raw_jobs(conn: Connection, df: pd.DataFrame):


    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")

    n = df.to_sql(
        "raw_jobs",
        conn,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    conn.commit()

    print(f"Inserted {n} rows into raw_jobs")