from rag.loader import load_rules
from rag.db import create_db
from config import DATA_PATH

def main():
    docs = load_rules(DATA_PATH)
    create_db(docs)
    print("DB built")

if __name__ == "__main__":
    main()