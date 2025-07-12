# frontend/main.py

import streamlit as st
import tempfile
from api.query_image import query_image
from api.query_llm import get_sql_from_llm
from api.run_sql import run_sql, run_ids_sql_query
from api.transcribe_audio import transcribe_audio
from utils.image_helper import make_entries_from_image_results, merge_records_with_distances
from st_audiorec import st_audiorec

def handle_transcription(audio_prompt):
    # print("Received audio bytes for transcription")
    # print(audio_prompt)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_prompt)
        tmp_path = tmp.name
    return transcribe_audio(tmp_path)

def run_text_search(query):
    sql = get_sql_from_llm(query)
    st.code(sql, language="sql")

    if sql.lower().startswith("select"):
        results = run_sql(sql)
        display_product_results(results)

    else:
        st.error("LLM did not return a SELECT query.")

def run_image_search(uploaded_img):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_img.read())
        tmp_path = tmp.name

    # 1. Query image search service → returns top-N similar embeddings with id + distance
    clip_results = query_image(tmp_path)

    # 2. Convert those into {category: [{id, distance}, ...]}
    entries = make_entries_from_image_results(clip_results)

    # 3. Fetch actual product data from the DB
    raw_result = run_ids_sql_query(entries)

    # 4. Merge and sort the results based on distance
    all_rows = []
    for block in raw_result:
        all_rows.extend(block["rows"])

    merged = merge_records_with_distances(all_rows, entries)

    # 5. Prepare result in format compatible with display
    results = [{"query": "image_search", "rows": merged}]
    display_product_results(results)



def display_product_results(products_sql_response: list):
    if not products_sql_response or not products_sql_response[0]["rows"]:
        st.warning("No products to display.")
        return

    st.markdown("## 🛒 Matching Products")
    rows = products_sql_response[0]["rows"]

    for product in rows:
        try:
            st.markdown("---")
            cols = st.columns([1, 4])

            # Image Display
            with cols[0]:
                st.image(product.get("image_url", ""), width=120)

            # Product Info
            with cols[1]:
                st.markdown(f"### {product.get('title', 'Unknown Product')}")
                st.markdown(f"- **Brand:** {product.get('brand', 'N/A')}")
                st.markdown(f"- **Price:** ₹{int(product.get('price', 0))}")
                if "distance" in product:
                    st.markdown(f"- **Similarity Distance:** `{product['distance']:.2f}`")
        except Exception as e:
            print(f"Error displaying product: {e}")
            continue

def main():
    st.set_page_config(page_title="Multimodal Product Search", layout="wide")
    st.title("🛍️ Search Products by Text | Image | Voice")

    # Layout: Text | Image | Voice
    col1, col2, col3 = st.columns([2, 2, 2])

    # Text Input Area
    with col1:
        st.markdown("#### 📝 Text Search")
        text_prompt = st.text_input("Type your query", placeholder="e.g. Laptops under 70k with touch screen")

    # Image Upload Area
    uploaded_img = None
    with col2:
        st.markdown("#### 🖼️ Image Search")
        uploaded_img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(uploaded_img, caption="Uploaded Image", width=200)

    # Voice Recording Area
    with col3:
        st.markdown("#### 🎙️ Voice Search")
        st.markdown("Click the button below to record your voice query.")

        audio_prompt = st_audiorec()

    # Unified Search Trigger
    st.markdown("---")
    st.markdown("### 📦 Search Results")

    # col4, col5 = st.columns([1, 1])
    option = st.selectbox("Select Search Method", options=["Text", "Image", "Voice"], key="search_method")
    if st.button("🔍 Search Now"):
        if option == "Voice":
            if audio_prompt:
                with st.spinner("Transcribing voice..."):
                    transcription = handle_transcription(audio_prompt)
                    st.success(f"You said: **{transcription}**")
                    run_text_search(transcription)
            else:
                st.warning("Voice input is empty. Please record your voice query.")

        elif option == "Text":
            if text_prompt:
                with st.spinner("Searching from text..."):
                    run_text_search(text_prompt)
            else:
                st.warning("Text input is empty. Please enter your query.")

        elif option == "Image":
            if uploaded_img:
                with st.spinner("Searching from image..."):
                    run_image_search(uploaded_img)
            else:
                st.warning("Image input is empty. Please upload an image.")
        else:
            st.warning("Please provide text, image, or voice input to search.")

if __name__ == "__main__":
    main()
