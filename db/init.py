# db/init.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from .models import Base  # Your SQLAlchemy models (User, Answer, PromoCode)

# Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Initialize DB (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)
