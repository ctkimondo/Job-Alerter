# Job Alerter

## Project Overview
A contanerized ETL pipeline that utilizes technologies to scrape jobs, compares job descriptions with a resume and alerts the user if the job is a high match so that the user can go ahead and apply.

# Data Engineering Architecture
Extraction (producer.py) - Connects to the API and scrapes the job data. The data is then served to kafka for utlization. 

Comparison (ai_matcher) - Utilizes the Google Gemini models to compare the resume with the job description and gives a match score.

Notifier (notifier.py) - Once a job is found, the user is notified on their preferred platform. For this project, I opted to use Discord for it's simplicity.

Consumer (main.py) - Utilizes the data from the extraction and comparison stages to save the data to a postgres database and uses the notifier to notify the user.

Contanerization - Fully packaged with Docker to ensure 100% reproduibility across any cloud environment.

# Getting Started
## Prerequisities
- Docker
- Python 3.11+
- The requirements.txt contains all libraries needed to pip install

## Running with Docker
pip install -r requirements.txt

docker compose up -d

Run this command in one terminal -> python src\main.py

Then run this command in another terminal -> python src\producer.py

This is because producer.py will extract data and send to kafka so that that data can be utilized by main.py.

# Future fixes
Search for free AI API that has more requests per day.

Look into why the same jobs keep repeating when produced.






