import streamlit as st

from rag.db import load_db
from rag.retriever import retrieve_with_score
from rag.reranker import rerank_rules
from llm.chain import build_chain


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Japanese AI Tutor", page_icon="🇯🇵")
st.title("🇯🇵 Japanese AI Tutor ")

# -----------------------------
# Init
# -----------------------------
db = load_db()
retriever = db.as_retriever()
chain = build_chain()

# -----------------------------
# Input
# -----------------------------
text = st.text_area("請輸入日文句子", height=150)

if st.button("開始分析"):

    if not text.strip():
        st.warning("請先輸入句子")
        st.stop()

    # =========================================================
    # 1. 先篩選 rules
    # =========================================================
    docs = retrieve_with_score(retriever, text)

    if not docs:
        st.error("沒有找到相關規則")
        st.stop()

    # =========================================================
    # 2. Reranking
    # =========================================================
    docs = rerank_rules(text, docs)

    # =========================================================
    # 3. Context Compression
    # =========================================================
    rules_text = ""

    for d in docs:
        if isinstance(d, dict):
            rules_text += d["content"] + "\n"
        else:
            rules_text += d.page_content + "\n"

    # =========================================================
    # 4. LLM Streaming
    # =========================================================
    st.subheader("AI 回覆")

    placeholder = st.empty()
    output = ""

    try:
        for chunk in chain.stream({
            "rules": rules_text,
            "input": text
        }):

            if hasattr(chunk, "content") and chunk.content:
                output += chunk.content
                placeholder.markdown(output)
        # =========================================================
        # 5. Debug
        # =========================================================
        with st.expander("📚 使用的規則 (debug)"):
            st.code(rules_text)

    except Exception as e:
        st.error(f"發生錯誤：{e}")

