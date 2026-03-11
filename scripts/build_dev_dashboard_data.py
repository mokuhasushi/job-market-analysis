import pandas as pd
from pathlib import Path
from src.db.connection import get_connection
from sqlalchemy import text

engine = get_connection()

OUTPUT_DIR = Path("dashboard/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_KEYWORDS = [
    "developer",
    "engineer",
    "data analyst",
    "data scientist",
    "devops",
    "backend",
    "frontend",
    "full stack",
    "machine learning",
    "data engineer"
]

ROLE_MAP = {
    "data analyst": "Data",
    "data scientist": "Data",
    "data engineer": "Data",
    "machine learning": "Data",

    "devops": "DevOps",

    "backend": "Software",
    "frontend": "Software",
    "full stack": "Software",
    "developer": "Software",
    "engineer": "Software"
}

def tech_job_filter_sql():

    conditions = [
        f"LOWER(title) LIKE '%{kw.lower()}%'" for kw in TARGET_KEYWORDS
    ]

    return " OR ".join(conditions)

def export_top_job_titles():

    filter_sql = tech_job_filter_sql()
    query = text(f"""
        SELECT title, COUNT(*) as jobs
        FROM jobs
        WHERE ({filter_sql})
        GROUP BY title
        ORDER BY jobs DESC
        LIMIT 20
    """)

    df = pd.read_sql(query, engine)

    df.to_parquet(OUTPUT_DIR / "top_job_titles.parquet")

def export_salary_distribution():

    filter_sql = tech_job_filter_sql()

    query = text(f"""
        SELECT salary_min
        FROM jobs
        WHERE salary_min IS NOT NULL
        AND ({filter_sql})
    """)

    df = pd.read_sql(query, engine)

    df.to_parquet(OUTPUT_DIR / "salary_distribution.parquet")

def export_jobs_by_country():

    filter_sql = tech_job_filter_sql()

    query = text(f"""
        SELECT l.country, COUNT(*) as jobs
        FROM jobs j
        JOIN locations l ON j.location_id = l.id
        WHERE ({filter_sql})
        GROUP BY l.country
        ORDER BY jobs DESC
    """)

    df = pd.read_sql(query, engine)

    df.to_parquet(OUTPUT_DIR / "jobs_by_country.parquet")


def export_salary_vs_experience():

    filter_sql = tech_job_filter_sql()

    query = text(f"""
        SELECT experience_level,
               AVG((salary_min + salary_max ) / 2.0) AS avg_salary
        FROM jobs
        WHERE salary_min IS NOT NULL
          AND salary_max IS NOT NULL
        AND ({filter_sql})
        GROUP BY experience_level
        ORDER BY experience_level
    """)

    df = pd.read_sql(query, engine)

    df.to_parquet(OUTPUT_DIR / "salary_vs_experience.parquet")

def export_salary_by_role():

    filter_sql = tech_job_filter_sql()

    query = text(f"""
        SELECT title,
               AVG((salary_min + salary_max ) / 2.0) AS avg_salary,
               COUNT(*) as jobs
        FROM jobs
        WHERE salary_min IS NOT NULL
          AND salary_max IS NOT NULL
        AND ({filter_sql})
        GROUP BY title
        HAVING COUNT(*) > 20
        ORDER BY avg_salary DESC
        LIMIT 20;
    """)

    df = pd.read_sql(query, engine)

    df.to_parquet(OUTPUT_DIR / "salary_by_role.parquet")


def run():

    print("Building dashboard datasets...")

    export_top_job_titles()
    export_salary_distribution()
    export_jobs_by_country()
    export_salary_vs_experience()
    export_salary_by_role()

    print("Dashboard datasets ready")


if __name__ == "__main__":
    run()

