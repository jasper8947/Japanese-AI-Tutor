from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL, DB_PATH, COLLECTION_NAME

embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_db(docs):
    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME
    )
    return db


def load_db():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding,
        collection_name=COLLECTION_NAME
    )