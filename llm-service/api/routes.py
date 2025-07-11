from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from llm.whisper_transcribe import transcribe_mp3
from llm.sql_query_generator import generate_sql
from models.schemas import PromptRequest, SQLResponse
import logging
import os
from datetime import datetime
import shutil

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-sql", response_model=SQLResponse)
def generate_sql_route(request: PromptRequest):
    try:
        sql = generate_sql(request.query)
        return {"sql": sql}
    except Exception as e:
        logger.exception("Error generating SQL")
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/transcribe-audio")
async def transcribe_route(file: UploadFile = File(...)):
    try:
        # Construct safe file path
        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file to disk
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Transcribe
        transcription = transcribe_mp3(file_path)

        # Clean up
        os.remove(file_path)

        return { "transcription": transcription }

    except Exception as e:
        logger.exception("❌ Error transcribing audio")
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/")
def root():
    return {"message": "LLM SQL Generator is running."}
