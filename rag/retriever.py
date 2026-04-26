from config import TOP_K

def retrieve_with_score(retriever, query, k=TOP_K, threshold=0.75):
    docs = retriever.vectorstore.similarity_search_with_score(query, k=k)

    filtered = [
        doc for doc, score in docs
        if score >= threshold
    ]

    if len(filtered) == 0:
        filtered = [docs[0][0]] if docs else []

    return filtered