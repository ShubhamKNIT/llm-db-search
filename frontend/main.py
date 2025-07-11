import streamlit as st
import tempfile
from api.query_llm import get_sql_from_llm
from api.run_sql import run_sql
from api.transcribe_audio import transcribe_audio
from streamlit_mic_recorder import mic_recorder

def handle_transcription(audio_bytes) -> str:
    """Save audio to disk and call backend API to transcribe."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes["bytes"])
        tmp_path = tmp.name
    return transcribe_audio(tmp_path)


def execute_search(query: str):
    """Run LLM → SQL → DB and display results."""
    with st.spinner("Generating SQL..."):
        sql = get_sql_from_llm(query)
        st.code(sql, language="sql")

    if sql.lower().startswith("select"):
        with st.spinner("Fetching results..."):
            results = run_sql(sql)
        if not results:
            st.warning("No results found.")
        else:
            for block in results:
                st.subheader(f"Results for: `{block['query']}`")
                st.dataframe(block["rows"])
    else:
        st.error("LLM did not return a SELECT query.")


def main():
    st.set_page_config(page_title="Product Search LLM", layout="wide")
    st.title("🛍️ Natural Language Product Search (Text + Voice)")

    col1, col2 = st.columns([2, 1])
    query = ""

    # 🎤 Voice recording
    with col2:
        st.markdown("### 🎙️ Voice Search")
        audio_bytes = mic_recorder(start_prompt="Click to Record", stop_prompt="Stop", key="mic")

    # 📝 Text input
    with col1:
        query = st.text_input("📝 Or type your query", placeholder="e.g., Laptops under 60k with touch screen")

    # 🎤 Handle voice transcription
    if audio_bytes:
        with st.spinner("Transcribing voice..."):
            transcription = handle_transcription(audio_bytes)
            query = transcription
            st.success(f"You said: **{transcription}**")
            execute_search(query)

    # 🔍 Unified Search Button
    if query and st.button("🔍 Search"):
        execute_search(query)


if __name__ == "__main__":
    main()
