from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://practiceuser:Qwertzuiop228c@localhost/practicedb'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(
    bind = engine,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

async def get_session_async():
    async with SessionLocal() as session:
        yield session