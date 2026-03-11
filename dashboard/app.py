import streamlit as st
import plotly.express as px
from queries import *

st.title("📊 Job Market Analyzer")

# By Title
st.subheader("Top Job Titles")

titles = top_job_titles()

fig = px.bar(
    titles,
    x="jobs",
    y="title",
    orientation="h"
)

st.plotly_chart(fig)

# By Country
st.subheader("Jobs by Country")

countries = jobs_by_country()

fig = px.bar(
    countries,
    x="country",
    y="jobs"
)

st.plotly_chart(fig)

# Salary Distribution
st.subheader("Salary Distribution")

salary = salary_distribution()

fig = px.histogram(
    salary,
    x="salary_min",
    nbins=40
)

st.plotly_chart(fig)


# Salary vs Experience

st.subheader("Average Salary by Experience")

exp = salary_vs_experience()

fig = px.bar(
    exp,
    x="experience_level",
    y="avg_salary"
)

st.plotly_chart(fig)