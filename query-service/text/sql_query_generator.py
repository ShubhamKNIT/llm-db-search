# query-service/text/sql_query_generator.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "llm-service"))

from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from text.sql_schema_prompt import SCHEMA
# import os
import logging
import re
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define expected output format
class SQLQueryRequest(BaseModel):
    sql: str

parser = JsonOutputParser(pydantic_object=SQLQueryRequest)


prompt = ChatPromptTemplate.from_messages([
    ("system", SCHEMA),
    ("human", "{query}")
])

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0.2
# )

llm = ChatOllama(
    model="llama3.2:latest",  # or "codellama"
    temperature=0.2
)

chain = prompt | llm | parser


def extract_select_query(text: str) -> str:
    match = re.search(r"SELECT\s.+", text, re.IGNORECASE | re.DOTALL)
    return match.group(0).strip() if match else "SELECT query not found in response."

def generate_sql(user_query: str) -> str:
    try:
        logger.info("Sending query to LLM: %s", user_query)
        full_query = user_query + "\nReturn only JSON: {\"sql\": \"SELECT ...\"}"
        response = chain.invoke({"query": full_query})
        logger.info("LLM response raw: %s", response)

        # Case 1: Already a dict
        if isinstance(response, dict):
            return response.get("sql", extract_select_query(str(response)))

        # Case 2: It's a string (fallback)
        try:
            response_json = json.loads(response)
            return response_json.get("sql", extract_select_query(response))
        except Exception:
            return extract_select_query(response)


    except Exception as e:
        logger.error(f"❌ Error generating SQL: {e}")
        return "An error occurred while generating SQL."
