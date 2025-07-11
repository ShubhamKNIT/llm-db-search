import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "llm-service"))

from huggingface_hub import InferenceClient
import os
from llm.sql_schema_prompt import SCHEMA


client = InferenceClient(
    provider="auto",
    api_key=os.environ["HF_TOKEN"]
)

def generate_sql(user_query: str) -> str:
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
        messages=[
            {
                "role": "system",
                "content": SCHEMA,
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
    )
    
    print("Generated SQL:", completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()
