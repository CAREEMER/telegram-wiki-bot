from sqlalchemy import literal_column, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def update_user(user_id: int, session: AsyncSession, **data):
    query = update(User).where(User.id == user_id).values(**data).returning(literal_column("*"))

    return (await session.execute(query)).first()
