import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text # <-- ADD 'text' HERE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- This is a temporary block for testing the connection ---
# We will remove this later, but it's useful for debugging now.
try:
    with engine.connect() as connection:
        # Use the text() construct for the SQL command
        connection.execute(text("SELECT 1"))
    print("--- Database connection successful! ---")
except Exception as e:
    print(f"--- Database connection failed: {e} ---")
# -----------------------------------------------------------