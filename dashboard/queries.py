import pandas as pd
from src.db.connection import get_connection

engine = get_connection()


def top_job_titles():

    query = """
    SELECT title, COUNT(*) as count
    FROM jobs
    GROUP BY title
    ORDER BY count DESC
    LIMIT 10
    """

    return pd.read_sql(query, engine)

def salary_distribution():

    query = """
    SELECT salary_min
    FROM jobs
    WHERE salary_min IS NOT NULL
    """

    return pd.read_sql(query, engine)

def jobs_by_country():

    query = """
    SELECT l.country, COUNT(*) as count
    FROM jobs j
    JOIN locations l ON j.location_id = l.id
    GROUP BY l.country
    ORDER BY count DESC
    """

    return pd.read_sql(query, engine)

def jobs_by_company_size():

    query = """
    SELECT c.company_size, COUNT(*)
    FROM jobs j
    JOIN companies c ON j.company_id = c.id
    GROUP BY c.company_size
    """

    return pd.read_sql(query, engine)

def salary_vs_experience():

    query = """
    SELECT experience_level,
           AVG(salary_min) as avg_salary
    FROM jobs
    WHERE salary_min IS NOT NULL
    GROUP BY experience_level
    """

    return pd.read_sql(query, engine)