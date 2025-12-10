from src.db import get_db


def main():
    db = get_db()
    print("Successfully connected to DB:", db.name)
    print("Existing collections:", db.list_collection_names())


if __name__ == "__main__":
    main()
