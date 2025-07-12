# frontend/api/run_sql.py

import requests
import os
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

DB_API_URL = os.getenv("DB_API_URL")
DB_IDS_API_URL = os.getenv("DB_IDS_API_URL")

def run_sql(sql: str):
    try:
        response = requests.post(DB_API_URL, json={"sql": sql})
        response.raise_for_status()
        print("✅ DB API response:", response.json())
        return response.json().get("results", [])
    except Exception as e:
        print("❌ DB API error:", e)
        return []
    
def run_ids_sql_query(ids: list):
    try:
        payload = {"entries": ids}
        response = requests.post(DB_IDS_API_URL, json=payload)
        response.raise_for_status()
        print("✅ DB IDS API response:", response.json())
        return response.json().get("results", [])[0].get("rows", [])
    except Exception as e:
        print("❌ DB IDS API error:", e)
        return []