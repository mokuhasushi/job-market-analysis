import pandas as pd
from pathlib import Path
from src.db.connection import get_connection

engine = get_connection()

OUTPUT_DIR = Path("dashboard/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_top_job_titles():

    df = pd.read_sql("""
        SELECT title, COUNT(*) as jobs
        FROM jobs
        GROUP BY title
        ORDER BY jobs DESC
        LIMIT 20
    """, engine)

    df.to_parquet(OUTPUT_DIR / "top_job_titles.parquet")


def export_salary_distribution():

    df = pd.read_sql("""
        SELECT salary_min
        FROM jobs
        WHERE salary_min IS NOT NULL
    """, engine)

    df.to_parquet(OUTPUT_DIR / "salary_distribution.parquet")


def export_jobs_by_country():

    df = pd.read_sql("""
        SELECT l.country, COUNT(*) as jobs
        FROM jobs j
        JOIN locations l ON j.location_id = l.id
        GROUP BY l.country
        ORDER BY jobs DESC
    """, engine)

    df.to_parquet(OUTPUT_DIR / "jobs_by_country.parquet")


def export_salary_vs_experience():

    df = pd.read_sql("""
        SELECT experience_level,
               AVG(salary_min) AS avg_salary
        FROM jobs
        WHERE salary_min IS NOT NULL
        GROUP BY experience_level
    """, engine)

    df.to_parquet(OUTPUT_DIR / "salary_vs_experience.parquet")


def run():

    print("Building dashboard datasets...")

    export_top_job_titles()
    export_salary_distribution()
    export_jobs_by_country()
    export_salary_vs_experience()

    print("Dashboard datasets ready")


if __name__ == "__main__":
    run()