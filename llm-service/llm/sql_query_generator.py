# llm-service/llm/sql_query_generator.py
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
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

SCHEMA = """
You are a SQL query generator for an e-commerce product database. 
Write simple SQL SELECT queries based on user input and do not add extra constraints.
The database has two tables: `mobiles` and `laptops`.
If you think there are multiple valid queries, separate them with a semicolon.
We are using PostgreSQL, so use the correct syntax for that database.
And also address case sensitivity in table and column names.
e.g, where lower(brand) = lower('Apple').
When you are making query for description or title then you must use regex matching with postgres.

Only return a valid JSON with the SQL query. Format must be exactly:
{{
  "sql": "<your sql here>"
}}
Allowed tables and columns:

TABLE: mobiles
- id (int)
- title (text)
- description (text)
- brand (text)
- ratings (float)
- ram (int, in GB)
- storage (int, in GB)
- battery (int, in mAh)
- screen (text)
- camera (text)
- graphics (text)
- processor (text)
- os (text)
- price (float)
- image_url (text)

TABLE: laptops
- id (int)
- title (text)
- description (text)
- brand (text)
- ratings (float)
- ram (int, in GB)
- storage (int, in GB)
- battery (int, in Wh)
- screen (text)
- touch_screen (boolean)
- graphics (text)
- processor (text)
- os (text)
- price (float)
- image_url (text)

Rules:
- ONLY generate SELECT queries
- DO NOT add any explanations or extra fields
- DO NOT wrap SQL in Markdown or code blocks
- DO NOT return 'thought', 'reasoning', etc.
"""

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
