from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import (
    create_db_tables,
    close_db_connection
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Application startup
    await create_db_tables()

    yield

    # Application shutdown
    await close_db_connection()