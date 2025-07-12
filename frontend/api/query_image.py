# frontend/api/query_image.py

import os
import requests
from dotenv import load_dotenv
load_dotenv()

IMAGE_API_URL = os.getenv("IMAGE_API_URL")
DB_IDS_API_URL = os.getenv("DB_IDS_API_URL")

def query_image(file_path: str):
    try:
        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f, "image/jpeg")}
            response = requests.post(IMAGE_API_URL, files=files)
        response.raise_for_status()
        results = response.json().get("results", [])
        print("✅ IMAGE API response:", results)
        return results
    except Exception as e:
        print("❌ IMAGE API error:", e)
        return []