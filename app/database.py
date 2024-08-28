from sqlalchemy import create_engine, MetaData
from databases import Database


DATABASE_URL = "sqlite:///./test.db"

try:
    database = Database(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
except Exception as e:
    print(f"Error connecting to database: {e}")

