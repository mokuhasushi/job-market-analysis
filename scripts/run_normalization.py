from src.etl.transform_raw_jobs import transform_france_switzerland_jobs
from src.db.connection import get_connection


def run():
    conn = get_connection()

    print("Transforming data for France and Switzerland...")

    transform_france_switzerland_jobs(conn)

    print("Done.")


if __name__ == "__main__":
    run()