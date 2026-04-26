import json
import time
import google.generativeai as genai

genai.configure(api_key="your_api_key")

model = genai.GenerativeModel("gemini-2.5-flash")

TOTAL_BATCH = 10      # 10次
BATCH_SIZE = 20      # 每次20條 = 200條

all_rules = []


def build_prompt(batch_id: int):
    return f"""
你是一位日文老師，請生成20條「中文母語者常犯的日文錯誤」。

範圍：第 {batch_id*20} ～ {(batch_id+1)*20} 條

必須遵守：
1. 每條必須具體（不能抽象如：注意語感）
2. 必須有錯誤句（wrong）
3. correct 必須是正確日文
4. explanation <= 50字中文
5. category 必須是：
   particle / verb / style / sentence

嚴格輸出 JSON array，不要 markdown，不要解釋

格式：

[
  {{
    "rule": "",
    "wrong": "",
    "correct": "",
    "explanation": "",
    "category": ""
  }}
]
"""


def clean_json(text: str):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")
    return text


for i in range(TOTAL_BATCH):
    print(f"🔄 generating batch {i+1}/{TOTAL_BATCH}")

    prompt = build_prompt(i)

    res = model.generate_content(prompt)

    try:
        text = clean_json(res.text)
        batch = json.loads(text)

        all_rules.extend(batch)

        print(f"✅ batch {i+1} ok, total = {len(all_rules)}")

    except Exception as e:
        print(f"❌ batch {i+1} failed:", e)

    time.sleep(1)  # 避免 API 壓力


# 💾 save final dataset
with open("data/grammar_rules.json", "w", encoding="utf-8") as f:
    json.dump(all_rules, f, ensure_ascii=False, indent=2)

print("🎉 DONE. Total rules:", len(all_rules))