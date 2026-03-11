import pandas as pd

DATA_PATH = "data/raw/job_descriptions.csv"

def load_raw_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    csv_to_final_columns={
        "Job Id": "id",
        "Experience": "experience_level",
        "Qualifications": "qualifications",
        "Salary Range": "salary",
        "Location": "location",
        "Country": "country",
        "Work Type": "employment_type",
        "Company Size": "company_size",
        "Job Posting Date": "posted_date",
        "Preference": "preference",
        "Job Title": "job_title",
        "Job Description": "description",
        "Skills": "skills",
        "Company": "company_name"
    }
    df = df.rename(columns=csv_to_final_columns)

    df = df[df.columns.intersection([csv_to_final_columns[k] for k in csv_to_final_columns])]

    return df
