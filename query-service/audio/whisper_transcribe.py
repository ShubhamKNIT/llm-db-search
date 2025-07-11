# query-service/audio/whisper_transcribe.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "llm-service"))

import whisper
from dotenv import load_dotenv
load_dotenv()

# Global model cache
model = None

def load_model():
    global model
    if model is None:
        model = whisper.load_model("tiny")  # options: tiny, base, small, medium, large

def transcribe_mp3(mp3_path: str) -> str:
    load_model()
    try:
        result = model.transcribe(mp3_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return ""
