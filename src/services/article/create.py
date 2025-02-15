from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Article, Draft
from schemas.draft import DraftStatusEnum
from services.article.content import create_content_from_draft
from services.draft.update import update_draft


async def create_article(session: AsyncSession) -> int:
    query = insert(Article).returning(Article.id)

    return (await session.execute(query)).scalars().first()


async def create_article_from_draft(draft: Draft, session: AsyncSession) -> int:
    await update_draft(draft_id=draft.id, status=DraftStatusEnum.DEPLOYED, session=session)
    new_article_id = await create_article(session)
    await create_content_from_draft(draft, new_article_id, session)
    return new_article_id


async def update_article_content_from_draft(draft: Draft, article_id: int, session: AsyncSession) -> int:
    await update_draft(draft_id=draft.id, status=DraftStatusEnum.DEPLOYED, session=session)
    await create_content_from_draft(draft, article_id, session)
    return article_id
