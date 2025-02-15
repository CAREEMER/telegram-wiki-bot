from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Article, ArticleTitle


async def perform_article_search(
    tokens: list[str], exclude_article_statuses: list[str], session: AsyncSession
) -> list[Article]:
    queries = []
    for token in tokens:
        queries.append(ArticleTitle.content.ilike(f"%{token}%"))

    query = (
        select(Article)
        .join(ArticleTitle, Article.id == ArticleTitle.article_id)
        .where(or_(*queries))
        .where(Article.status.notin_(exclude_article_statuses))
        .options(selectinload(Article.titles))
    )

    return (await session.execute(query)).scalars().all()
