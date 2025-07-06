# llm-service/main.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "llm-service"))

from fastapi import FastAPI, Request
from pydantic import BaseModel
from llm.sql_query_generator import generate_sql
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LLM_PORT = int(os.getenv("LLM_PORT"))

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    query: str

class SQLResponse(BaseModel):
    sql: str

@app.post("/generate-sql", response_model=SQLResponse)
def generate_sql_route(request: PromptRequest):
    try:
        sql = generate_sql(request.query)
        return {"sql": sql}
    except Exception as e:
        logger.error(f"❌ Error in /generate-sql route: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "LLM SQL Generator is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=LLM_PORT, reload=True)
