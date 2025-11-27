from .database import SessionLocal
from typing import Generator

# Dependency function to provide a database session for FastAPI routes
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

