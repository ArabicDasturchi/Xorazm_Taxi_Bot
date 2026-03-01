import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

from .models import Base

load_dotenv()
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///taxi_bot.sqlite")

engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        # Create all tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
        
        # Add custom columns via migration silently
        from sqlalchemy import text
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN custom_ad_message TEXT"))
        except Exception:
            pass

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
