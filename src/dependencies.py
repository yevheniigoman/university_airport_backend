from db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session