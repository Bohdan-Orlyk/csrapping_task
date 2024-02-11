import asyncpg

from config import db_config
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_session():
    session = await asyncpg.connect(
        user=db_config.user,
        password=db_config.password,
        database=db_config.database,
        host=db_config.host,
        port=db_config.port
    )

    try:
        yield session
    finally:
        await session.close()


