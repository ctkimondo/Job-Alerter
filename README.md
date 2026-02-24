# Job Alerter

## Project Overview
A containerized ETL pipeline designed to automate the job search process. The system scrapes real-time job listings, performs semantic analysis against a candidate's resume using LLMs, and delivers high-match alerts via Discord.

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
- Google Gemini API key
- Adzuna API Credentials
- The requirements.txt contains all libraries needed to pip install

## Running with Docker
pip install -r requirements.txt

docker compose up -d

Run this command in one terminal -> python src\main.py

Then run this command in another terminal -> python src\producer.py

This is because producer.py will extract data and send to kafka so that that data can be utilized by main.py.

# Technical Stack
Language: Python 3.11+

Orchestration: Docker, Docker Compose

Message Broker: Apache Kafka

Database: PostgreSQL

AI/ML: Google Gemini API (Generative AI)

Notifications: Discord Webhooks


# Future fixes
Search for free AI API that has more requests per day.

Look into why the same jobs keep repeating when produced.






