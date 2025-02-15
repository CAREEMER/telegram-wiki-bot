from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Draft, User
from schemas.draft import DraftStatusEnum


async def create_draft(redactor: User, session: AsyncSession, origin_article_id: int | None = None) -> Draft:
    query = (
        insert(Draft)
        .values(redactor_id=redactor.id, status=DraftStatusEnum.CREATED, origin_article_id=origin_article_id)
        .returning(Draft)
    )

    return (await session.execute(query)).scalars().one()
