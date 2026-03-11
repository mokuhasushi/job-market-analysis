import requests
from bs4 import BeautifulSoup

url = "https://example-job-site.com/jobs"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []

for job in soup.select(".job-card"):
    title = job.select_one(".title").text
    company = job.select_one(".company").text
    location = job.select_one(".location").text

    jobs.append({
        "title": title,
        "company": company,
        "location": location
    })

print(jobs)