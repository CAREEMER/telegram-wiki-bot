from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Draft


async def get_draft(draft_id: int, session: AsyncSession) -> Draft:
    query = (
        select(Draft)
        .where(Draft.id == draft_id)
        .options(selectinload(Draft.titles))
        .options(selectinload(Draft.texts))
        .options(selectinload(Draft.medias))
    )

    return (await session.execute(query)).scalars().one()
