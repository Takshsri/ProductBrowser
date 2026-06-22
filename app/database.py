from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)