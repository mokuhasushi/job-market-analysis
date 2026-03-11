from src.etl.load_dataset import load_raw_data
from src.etl.load_to_db import  insert_raw_jobs
from src.db.connection import get_connection


def run():

    print("Loading CSV...")
    df = load_raw_data()

    conn = get_connection()

    print("Inserting into database...")
    insert_raw_jobs(conn, df)


if __name__ == "__main__":
    run()