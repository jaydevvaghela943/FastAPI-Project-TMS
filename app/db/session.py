#Async engine,session maker
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine

#Get settings from /app/core/config.py
from app.core.config import settings

from app.db.base import Base

#Create engine for connection
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = settings.DEBUG,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 20
)

#Local Session Setup
AsyncSessionLocal = async_sessionmaker(bind=engine,autoflush=False,class_=AsyncSession,expire_on_commit=False)

# Create all database tables
async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


# Close database connection
async def close_db_connection():
    await engine.dispose()