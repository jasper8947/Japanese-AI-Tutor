from sentence_transformers import CrossEncoder

# =========================================================
# 1. CROSS ENCODER (LANGCHAIN-FRIENDLY)
# =========================================================
reranker = CrossEncoder("BAAI/bge-reranker-large")


# =========================================================
# 2. RERANK FUNCTION
# =========================================================
def rerank_rules(query, docs, top_k=2):

    texts = [
        d["content"] if isinstance(d, dict) else d.page_content
        for d in docs
    ]

    pairs = [(query, text) for text in texts]

    # cross encoder scoring
    scores = reranker.predict(pairs)

    # combine
    scored_docs = list(zip(scores, docs))

    # sort desc
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for _, doc in scored_docs[:top_k]]