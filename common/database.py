from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constant_helper import DATABASE_URL



DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
