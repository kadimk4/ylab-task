from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASS

engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=False)
session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_async_db() -> AsyncGenerator:
    db = session()
    try:
        yield db
    finally:
        await db.close()
