from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from lira_backend_api.settings import settings

import databases
from databases.core import Connection


# ASYNC Changes
LIRA_ASYNC_URL = str(settings.db_url("lira_db"))
ALTITUDE_ASYNC_URL = str(settings.db_url("altitude_db"))

lira_database = databases.Database(LIRA_ASYNC_URL)
altitude_database = databases.Database(ALTITUDE_ASYNC_URL)

lira_async_engine = create_async_engine(LIRA_ASYNC_URL, pool_pre_ping=True)
altitude_async_engine = create_async_engine(ALTITUDE_ASYNC_URL, pool_pre_ping=True)

# TODO: Investigate the Azure DB setup to create the model, schemas, and Base metadata object; create Altitude Base Object
Base = declarative_base()

# TODO: Hook up Altitude Base Object to DB
async def setup_db():
    async with lira_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# TODO: Create get_connection() for Altitude DB as well; focusing on Lira DB first
async def get_connection() -> Connection:
    async with lira_database.connection() as connection:
        yield connection


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# POSTGRES_DATABASE_URL = str(settings.db_url)

# engine = create_engine(POSTGRES_DATABASE_URL, pool_pre_ping=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# Base.metadata.reflect(bind=engine)
# Base.metadata.create_all(bind=engine)


# def get_db() -> Generator:  # new
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
