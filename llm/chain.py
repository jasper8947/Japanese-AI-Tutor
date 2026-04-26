from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from llm.prompt import prompt
from config import (
    LLM_PROVIDER,
    GEMINI_MODEL,
    OLLAMA_MODEL,
    GEMINI_API_KEY
)

def build_chain():

    if LLM_PROVIDER == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.2
        )

    elif LLM_PROVIDER == "ollama":
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0.2
        )

    else:
        raise ValueError("Unknown LLM_PROVIDER")

    return prompt | llm