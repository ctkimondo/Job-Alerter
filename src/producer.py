import requests
import json
import time
import os
from dotenv import load_dotenv

from kafka import KafkaProducer

load_dotenv()

def get_kafka_producer():
    # We connect to localhost:9092
    return KafkaProducer(
        bootstrap_servers=['localhost:9093'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

# Get credentials from env files
api_id = os.getenv('ADZUNA_API_ID')
api_key = os.getenv('ADZUNA_API_KEY')

def fetch_jobs():
    producer = get_kafka_producer()

    for page in range(1, 4):
        # Adzuna API URL
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}?app_id={api_id}&app_key={api_key}&what=data%20engineer%20intern"

        try:
            response = requests.get(url)
            data = response.json()
            jobs = data.get('results', [])

            for job in jobs:
                # Create clean job records
                job_data = {
                    "id": job.get('id'),
                    "title": job.get('title'),
                    "description": job.get('description'),
                    "link": job.get('redirect_url'),
                    "company": job.get('company', {}).get('display_name'),
                    "location": job.get('location', {}).get('location'),
                    "timestamp": time.time()
                }

                # Send to Kafka
                future = producer.send('job_listings', value=job_data)
                try:
                    record_metadata = future.get(timeout=10)
                    print(f"Sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
                except Exception as e:
                    print(f"Failed to send: {e}")
                print(f"Sent job to Kafka: {job_data['title']}")
            
            # Ensure all messages are actually sent before closing
            producer.flush()

        except Exception as e:
            print(f"Error fetching jobs: {e}")

    producer.close()
    
if __name__=="__main__":
    fetch_jobs()
