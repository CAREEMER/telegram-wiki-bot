from aiogram import types
from sqlalchemy import Row, insert, literal_column, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def get_user(user_data: types.User, session: AsyncSession) -> User | None:
    select_query = select(User).where(User.telegram_id == str(user_data.id))
    user = (await session.execute(select_query)).scalars().one_or_none()

    if not user:
        return

    if any((user.full_name != user_data.full_name, user.username != user_data.username)):
        values = {
            "full_name": user_data.full_name,
            "username": user_data.username,
            "mention": "@" + user_data.username if user_data.username else None,
        }
        await session.execute(update(User).values(**values).where(User.id == user.id))
        await session.refresh(user)

    return user


async def create_user(user_data: types.User, session: AsyncSession) -> Row[User]:
    user_insert_query = (
        insert(User)
        .values(
            telegram_id=str(user_data.id),
            username=user_data.username,
            mention="@" + user_data.username if user_data.username else None,
            full_name=user_data.full_name,
        )
        .returning(literal_column("*"))
    )

    return (await session.execute(user_insert_query)).one()


async def get_or_create_user(user_data: types.User, session: AsyncSession) -> User:
    return await get_user(user_data, session) or await create_user(user_data, session)
