# query-service/models/schemas.py

from pydantic import BaseModel

class PromptRequest(BaseModel):
    query: str

class SQLResponse(BaseModel):
    sql: str
