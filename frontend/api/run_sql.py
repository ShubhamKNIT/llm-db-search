# frontend/api/run_sql.py

import requests
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
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

def run_ids_sql_query(category_map: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    try:
        print("📦 Sending category_map:", category_map)
        payload = {"entries": category_map}
        response = requests.post(DB_IDS_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print("✅ DB IDS API response:", data)
        return data.get("results", [])
    except Exception as e:
        print("❌ DB IDS API error:", e)
        return []