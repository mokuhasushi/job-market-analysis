
# Install dependencies and setup
(venv) pip install -r requirements.txt
psql -d jobs -f db/schema.sql
create .env
Note: BigSerial

# Getting the data 
Set up Kaggle API TOKEN 
kaggle datasets download -d ravindrasinghrana/job-description-dataset

# Load as raw data 
python -m scripts/run_ingestion.py

# Transformation and Normalization 
Only for France and Switzerland to reduce compute time and since this is were I am looking for a job
(\d+\.?\d*) matches all group of digits with a . 

# Deploy on streamlit
with parquet

# Not very useful... target dev!

But hey, base dataset is fake data. Let's look for a real one
