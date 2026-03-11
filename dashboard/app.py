import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_DIR = Path("dashboard/data")

st.set_page_config(page_title="Job Market Analyzer", layout="wide")

st.title("Job Market Analyzer")

# Top job titles
titles = pd.read_parquet(DATA_DIR / "top_job_titles.parquet")

fig_titles = px.bar(
    titles,
    x="jobs",
    y="title",
    orientation="h"
)

st.subheader("Top Job Titles")
st.plotly_chart(fig_titles, use_container_width=True)

# Jobs by country
countries = pd.read_parquet(DATA_DIR / "jobs_by_country.parquet")

fig_country = px.bar(
    countries,
    x="country",
    y="jobs"
)

st.subheader("Jobs by Country")
st.plotly_chart(fig_country, use_container_width=True)

# Salary distribution
salary = pd.read_parquet(DATA_DIR / "salary_distribution.parquet")

fig_salary = px.histogram(
    salary,
    x="salary_min",
    nbins=40
)

st.subheader("Salary Distribution")
st.plotly_chart(fig_salary, use_container_width=True)

# Salary vs experience
exp = pd.read_parquet(DATA_DIR / "salary_vs_experience.parquet")

fig_exp = px.bar(
    exp,
    x="experience_level",
    y="avg_salary"
)

st.subheader("Average Salary by Experience")
st.plotly_chart(fig_exp, use_container_width=True)

# Salary by role
exp = pd.read_parquet(DATA_DIR / "salary_by_role.parquet")

fig_exp = px.bar(
    exp,
    x="title",
    y="avg_salary"
)

st.subheader("Average Salary by Role")
st.plotly_chart(fig_exp, use_container_width=True)