# frontend/api/transcribe_audio.py

import requests
import os
from dotenv import load_dotenv
load_dotenv()

TRANSCRIBE_API_URL = os.getenv("TRANSCRIBE_API_URL")

def transcribe_audio(file_path: str):
    try:
        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f, "audio/mpeg")}
            response = requests.post(TRANSCRIBE_API_URL, files=files)
        response.raise_for_status()
        return response.json().get("transcription", "")
    except Exception as e:
        print("❌ TRANSCRIBE API error:", e)
        return ""
