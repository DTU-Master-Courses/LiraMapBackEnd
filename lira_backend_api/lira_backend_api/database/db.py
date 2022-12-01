# Main Dev: PossibleNPC
# Supporting Devs: Mikfor, Tswagerman, wangrandk, HUIYULEO, ViktorRindom
from sqlalchemy.ext.declarative import declarative_base
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

Base = declarative_base()

async def setup_db():
    async with lira_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_connection() -> Connection:
    async with lira_database.connection() as connection:
        yield connection
