import json
from langchain_core.documents import Document


def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []

    for i, r in enumerate(data):

        # 用於 embedding
        retrieval_text = f"""
Wrong: {r['wrong']}
Correct: {r['correct']}
Rule: {r['rule']}
""".strip()

        # 用於 LLM（可選存 metadata 或 prompt）
        docs.append(
            Document(
                page_content=retrieval_text,
                metadata={
                    "category": r["category"],
                    "id": i,

                    "full_rule": r["rule"],
                    "correct": r["correct"],
                    "explanation": r["explanation"]
                }
            )
        )

    return docs