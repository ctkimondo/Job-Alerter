from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Reads the resume
def load_resume(file_path="data/resume.txt"):
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()

# Gets job score
def get_job_score(job_desc, resume_txt):
    # Looks for the GEMINI API KEY env var
    client = genai.Client()

    model_id = "gemini-flash-latest"

    prompt = f"""
    You are an expert Technical Recruiter
    Compare the following Job Description against the Candidate Resume

    RESUME:
    {resume_txt}

    JOB DESCRIPTION:
    {job_desc}

    Provide a match score (0-100) and short reason why.
    Format your response exactly like this:
    Score: [number]
    Reason: [sentence]
    """
    try:
        response= client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Testing  
if __name__ == "__main__":
    test_resume = "Python, SQL, Data Engineering"
    test_job = "Looking for a Data Engineer with Python skills."
    print(get_job_score(test_job, test_resume))


