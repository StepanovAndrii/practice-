from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.database import AsyncSessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session