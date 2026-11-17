from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

# Get DB : Connection check : 
#Every API request that uses Depends(get_db) receives a database session. When the request finishes, the session is closed automatically.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session