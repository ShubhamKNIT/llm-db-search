# llm-service/api/generate_sql.py
import requests 
from dotenv import load_dotenv
import os
import logging

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sql_from_llm(nl_query: str) -> str:
    try:
        response = requests.post(
            LLM_API_URL,
            json={"query": nl_query},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["sql"]
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request error generating SQL with LLM: {e}")
        return "An error occurred while generating SQL."
    except Exception as e:
        logger.error(f"❌ Unexpected error generating SQL with LLM: {e}")
        return "An unexpected error occurred."