# query-service/image/search_image.py

import os
import faiss
import json
import torch
from image.embedding_generator import model, preprocess_image

def search_similar_images(query_image_path, top_k=5):
    # Load FAISS index and metadata
    index = faiss.read_index(os.getenv("FAISS_INDEX_PATH", "faiss_index.index"))
    with open(os.getenv("FAISS_METADATA_PATH", "product_metadata.json"), "r") as f:
        metadata = json.load(f)

    # Preprocess the query image
    inputs = preprocess_image(query_image_path)
    if inputs is None:
        print("❌ Invalid query image.")
        return []

    # Get query embedding
    with torch.no_grad():
        query_embedding = model.get_image_features(**inputs)
        query_vector = query_embedding[0].cpu().numpy().astype("float32").reshape(1, -1)

    # Search in FAISS
    distances, indices = index.search(query_vector, top_k)

    # Collect results
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        item = metadata[idx]
        item["distance"] = float(dist)
        results.append(item)

    return results

