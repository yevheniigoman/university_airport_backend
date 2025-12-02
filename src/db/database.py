from config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(get_settings().DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)