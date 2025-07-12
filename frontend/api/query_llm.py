# frontend/api/query_llm.py

import os
import requests
from dotenv import load_dotenv
load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")

def get_sql_from_llm(nl_query: str) -> str:
    try:
        response = requests.post(LLM_API_URL, json={"query": nl_query})
        response.raise_for_status()
        print("✅ LLM API response:", response.json())
        return response.json().get("sql", "")
    except Exception as e:
        print("❌ LLM API error:", e)
        return ""
