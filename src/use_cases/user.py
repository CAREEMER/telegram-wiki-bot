from sqlalchemy.ext.asyncio import AsyncSession

from services.user.update import update_user


async def set_language_init(user_id: int, language_id: int, session: AsyncSession):
    return await update_user(user_id, session, language_id=language_id)
