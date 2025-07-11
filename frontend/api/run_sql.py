import requests
import os
from dotenv import load_dotenv
load_dotenv()

DB_API_URL = os.getenv("DB_API_URL")

def run_sql(sql: str):
    try:
        response = requests.post(DB_API_URL, json={"sql": sql})
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print("❌ DB API error:", e)
        return []