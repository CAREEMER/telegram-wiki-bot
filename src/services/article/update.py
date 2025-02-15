from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Article


async def update_article(article_id: int, session: AsyncSession, **kwargs) -> None:
    query = update(Article).where(Article.id == article_id).values(**kwargs)
    await session.execute(query)
