import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# This line loads the variables from your .env file
load_dotenv()

# This gets the database URL from the environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# This is our test to make sure the right URL is being used
print(f"--- DATABASE URL BEING USED: {SQLALCHEMY_DATABASE_URL} ---")

# This is the main engine that connects SQLAlchemy to your database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates a "session" class, which is what we'll use to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is a base class that our database models will inherit from
Base = declarative_base()