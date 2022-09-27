from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from lira_backend_api.settings import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
POSTGRES_DATABASE_URL = str(settings.db_url)

engine = create_engine(
    POSTGRES_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Base.metadata.reflect(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

