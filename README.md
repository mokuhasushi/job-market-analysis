
# Install dependencies and setup
(venv) pip install -r requirements.txt
psql -d jobs -f db/schema.sql
create .env

# Getting the data 
Set up Kaggle API TOKEN 
kaggle datasets download -d ravindrasinghrana/job-description-dataset

# Set up the db connection 
define schema
