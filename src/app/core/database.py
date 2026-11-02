from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://user:password@localhost:5432/practive'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

AsyncSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)