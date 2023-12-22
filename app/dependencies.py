from app.database import session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


async def get_session() -> Session | AsyncSession:
    """
    Database dependency: allows a single Session per request.
    """   
    yield session