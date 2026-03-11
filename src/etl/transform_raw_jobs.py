import pandas as pd
from sqlalchemy import text, Connection
from src.db.connection import get_connection
import re


def parse_salary(s):
    if pd.isna(s):
        return None, None, None
    # Example: "$80k - $120k"
    match = re.findall(r'(\d+\.?\d*)', str(s))
    if len(match) == 0:
        return None, None, None
    min_salary = int(match[0])*1000
    max_salary = int(match[1])*1000 if len(match) > 1 else min_salary
    currency = "USD" if "$" in s else "EUR" if "€" in s else None
    return min_salary, max_salary, currency





def transform_france_switzerland_jobs(conn: Connection):

    print("Reading db for raw jobs...")
    df = pd.read_sql("SELECT * FROM raw_jobs WHERE country = 'France' OR country = 'Switzerland'" , conn)

    df = df.drop_duplicates()
    df["salary_min"], df["salary_max"], df["salary_currency"] = zip(*df["salary"].map(parse_salary))

    print("Insert companies...")

    companies = df[["company_name", "company_size"]].drop_duplicates()

    for _, row in companies.iterrows():
        res = conn.execute(
            text("""
            INSERT INTO companies (name, company_size) VALUES (:name, :size)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """), {"name": row["company_name"], "size": row["company_size"]}
        )

    print("Insert locations...")

    locations = df[["location", "country"]].drop_duplicates()

    for _, row in locations.iterrows():
        res = conn.execute(
            text("""
            INSERT INTO locations (city, country) VALUES (:city, :country)
            ON CONFLICT DO NOTHING
            RETURNING id
            """), {"city": row["location"], "country": row["country"]}
        )

    print("Insert jobs...")

    for _, row in df.iterrows():
        # Get company_id
        company_id = conn.execute(
            text("SELECT id FROM companies WHERE name=:name"),
            {"name": row["company_name"]}
        ).scalar()
        
        location_id = conn.execute(
            text("SELECT id FROM locations WHERE city=:city AND country=:country"),
            {"city": row["location"], "country": row["country"]}
        ).scalar()
        
        conn.execute(
            text("""
            INSERT INTO jobs (
                id, title, description, qualifications, experience_level, employment_type, 
                preference, salary_min, salary_max, salary_currency, posted_date,
                company_id, location_id
            ) VALUES (
                :id, :title, :desc, :qual, :exp, :etype, :pref, :smin, :smax, :curr, :pdate, :cid, :lid
            )
            """), {
                "id": row["id"],
                "title": row["job_title"],
                "desc": row["description"],
                "qual": row["qualifications"],
                "exp": row["experience_level"],
                "etype": row["employment_type"],
                "pref": row["preference"],
                "smin": row["salary_min"],
                "smax": row["salary_max"],
                "curr": row["salary_currency"],
                "pdate": row["posted_date"],
                "cid": company_id,
                "lid": location_id
            }
        )

    print("Insert skills...")

    skills_list = df["skills"].dropna().str.split(",")
    skills_set = set([s.strip().lower() for sublist in skills_list for s in sublist])

    for skill in skills_set:
        conn.execute(
            text("""
            INSERT INTO skills (skill_name) VALUES (:skill)
            ON CONFLICT (skill_name) DO NOTHING
            """), {"skill": skill}
        )

    for _, row in df.iterrows():
        job_id = row["id"]
        
        if pd.notna(row["skills"]):
            for skill in row["skills"].split(","):
                skill = skill.strip().lower()
                skill_id = conn.execute(
                    text("SELECT id FROM skills WHERE skill_name=:skill"),
                    {"skill": skill}
                ).scalar()
                
                conn.execute(
                    text("INSERT INTO job_skills (job_id, skill_id) VALUES (:jid, :sid) ON CONFLICT DO NOTHING"),
                    {"jid": job_id, "sid": skill_id}
                )

    conn.commit()