CREATE SCHEMA jobs;

CREATE TABLE jobs.companies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE, 
    company_size TEXT
);

CREATE TABLE jobs.locations (
    id SERIAL PRIMARY KEY,
    city TEXT,
    country TEXT
);

CREATE TABLE jobs.raw_jobs (
    id BIGSERIAL PRIMARY KEY,
    experience_level TEXT,
    qualifications TEXT,
    salary TEXT, 
    location TEXT,
    country TEXT,
    employment_type TEXT,
    company_size TEXT,
    posted_date DATE, 
    preference TEXT,
    job_title TEXT,
    description TEXT,
    skills TEXT,
    company_name TEXT
);

CREATE TABLE jobs.jobs (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    qualifications TEXT,

    company_id INT REFERENCES jobs.companies(id),

    location_id INT REFERENCES jobs.locations(id),

    employment_type TEXT,
    preference TEXT,
    experience_level TEXT,

    salary_min INT, 
    salary_max INT, 
    salary_currency TEXT, 
    salary_raw TEXT, 

    posted_date DATE 
);

CREATE TABLE jobs.skills (
    id SERIAL PRIMARY KEY,
    skill_name TEXT UNIQUE
);

CREATE TABLE jobs.job_skills (
    job_id BIGINT REFERENCES jobs.jobs(id),
    skill_id INT REFERENCES jobs.skills(id),
    PRIMARY KEY (job_id, skill_id)
);


CREATE INDEX idx_raw_jobs_title ON jobs.raw_jobs(job_title);
CREATE INDEX idx_raw_jobs_company ON jobs.raw_jobs(company_name);
CREATE INDEX idx_raw_jobs_location ON jobs.raw_jobs(location);