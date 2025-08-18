# query-service/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
import logging
import os
import uvicorn

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load environment
load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Entrypoint
if __name__ == "__main__":
    port = int(os.getenv("LLM_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
