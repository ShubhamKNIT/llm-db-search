# query-service/image/embedding_generator.py

import os
import json
import torch
import faiss
import psycopg2
from PIL import Image
from dotenv import load_dotenv
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel

# Load environment variables
load_dotenv()

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Image preprocessing
def preprocess_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt", padding=True)
        return inputs.to(device)
    except Exception as e:
        print(f"⚠️ Failed to preprocess {image_path}: {e}")
        return None

# Load products from PostgreSQL
def load_products():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5433),
    )
    cursor = conn.cursor()
    all_rows = []

    for category in ["mobiles", "laptops"]:
        cursor.execute(f"SELECT id, title, image_url, brand, price FROM {category} WHERE image_url IS NOT NULL")
        rows = cursor.fetchall()
        for row in rows:
            id, title, image_url, brand, price = row
            all_rows.append({
                "id": id,
                "title": title,
                "category": category,
                "image_url": image_url,
                "brand": brand,
                "price": price
            })

    cursor.close()
    conn.close()
    return all_rows

# Build and save FAISS index
def build_faiss_index():
    metadata = []
    vectors = []

    products = load_products()
    print(f"🖼️ Processing {len(products)} products...")

    for i, product in enumerate(products):
        image_path = product["image_url"]

        if not os.path.exists(image_path):
            print(f"[{i+1}] ❌ Image not found: {image_path}")
            continue

        inputs = preprocess_image(image_path)
        if inputs is None:
            continue

        try:
            with torch.no_grad():
                image_features = model.get_image_features(**inputs)
                embedding = image_features[0].cpu().numpy().astype("float32")
                vectors.append(embedding)

                metadata.append({
                    "id": product["id"],
                    "title": product["title"],
                    "category": product["category"],
                    "image_url": product["image_url"],
                    "brand": product["brand"],
                    "price": product["price"]
                })

                print(f"[{i+1}/{len(products)}] ✅ Processed: {product['title']}")

        except Exception as e:
            print(f"[{i+1}] ⚠️ Error processing image: {e}")

    # FAISS index creation
    if vectors:
        dim = len(vectors[0])
        index = faiss.IndexFlatL2(dim)
        index.add(torch.tensor(vectors).numpy())

        faiss.write_index(index, "image_index.faiss")
        with open("product_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"\n✅ Indexed {len(metadata)} products into FAISS and saved metadata.json")
    else:
        print("❌ No valid vectors to index.")

if __name__ == "__main__":
    build_faiss_index()
