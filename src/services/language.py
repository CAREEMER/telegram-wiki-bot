from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Language


async def list_languages(session: AsyncSession) -> list[Language]:
    return (await session.execute(select(Language).order_by(Language.is_primary.desc()))).scalars().all()


async def get_primary_language(session: AsyncSession) -> Language:
    return (await session.execute(select(Language).where(Language.is_primary.is_(True)))).scalars().first()


async def get_language(language_id: int, session: AsyncSession) -> Language:
    return (await session.execute(select(Language).where(Language.id == language_id))).scalars().one()
