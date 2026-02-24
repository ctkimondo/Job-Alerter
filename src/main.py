# Consumer!

# Takes the jobs that were scraped using the API 
# From kafka and into AI for the score then into postgres
import json
import re
import time
import os
from kafka import KafkaConsumer
from notifier import send_alert
from ai_matcher import get_job_score, load_resume
from connectdb import connect_to_db

def start_consumer():
    # Load up resume
    print("Loading resume")
    try:
        resume_txt = load_resume()
    except Exception as e:
        print("Could not find resume.txt: {e}")
        return

    # Setup the Postgres connection
    conn = connect_to_db()
    if not conn: return
    cur = conn.cursor()

    # Setup the Kafka listener
    consumer = KafkaConsumer(
        'job_listings',
        bootstrap_servers=['localhost:9093'],
        auto_offset_reset='earliest', # Start from the first job
        # group_id='job-cous-343535', # Keeps track of what we've already read
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    create_table_query = """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                company TEXT,
                description TEXT,
                link TEXT,
                ai_score INTEGER);"""
    
    cur.execute(create_table_query)
    conn.commit()

    print("Consumer started. Looking for jobs.")
    
    try:
        for message in consumer:
            print("RECEIVED!")
            job = message.value
            title = job.get('title')
            company = job.get('company')

            print(f"\n Analyzing: {title} @ {company}")

            # Process job with AI
            ai_output = get_job_score(job.get('description'), resume_txt)
            print(f"ai_output raw: {ai_output}")

            # Extract score using Regex
            score_match = re.search(r"Score:\s*(\d+)", ai_output)
            score = int(score_match.group(1)) if score_match else 0

            # Extract Reason
            reason_match = re.search(r"Reason:\s*(.*)", ai_output)
            reason = reason_match.group(1) if reason_match else "No reason given."

            # SQL!!
            # Save the job and the ai score
            # Use "ON CONFLICT" to handle duplicates
            
            insert_query = """
            INSERT INTO jobs (job_id, title, company, description, link, ai_score)
            VALUES(%s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) 
            DO UPDATE SET ai_score = EXCLUDED.ai_score;
            """

            cur.execute(insert_query, (
                job.get('id'),
                job.get('title'),
                job.get('company'),
                job.get('description'),
                job.get('link'),
                score
            )) 

            # Save, print
            conn.commit()
            print(f"Saved to DB: {job.get('title')}")

            # Notification step
            if score >= 70:
                print(f"High Match ({score})! Pinging Discord")
                send_alert(title, company, score, reason, job.get('link'))
            else:
                print(f"Match Score: {score}. Logged to database")

            # Gemini API Rate Limit
            # Limit: 15 RPM = 1 request every 4 seconds
            time.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    start_consumer()