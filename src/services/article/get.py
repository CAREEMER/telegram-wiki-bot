from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Article, MainArticle
from schemas.article import ArticleStatusEnum


async def get_article(article_id: int, session: AsyncSession) -> Article | None:
    return (
        (
            await session.execute(
                select(Article)
                .where(Article.id == article_id)
                .options(selectinload(Article.titles))
                .options(selectinload(Article.texts))
                .options(selectinload(Article.medias))
            )
        )
        .scalars()
        .one_or_none()
    )


async def get_main_articles(session: AsyncSession) -> list[Article]:
    query = select(Article).join(MainArticle).options(selectinload(Article.titles)).order_by(MainArticle.order_by)
    return (await session.execute(query)).scalars().all()


async def list_articles(
    excluded_article_statuses: list[ArticleStatusEnum],
    page: int,
    size: int,
    session: AsyncSession,
) -> list[Article]:
    query = (
        select(Article)
        .where(Article.status.notin_(excluded_article_statuses))
        .options(selectinload(Article.titles))
        .offset(size * page)
        .limit(size + 1)
    )

    return (await session.execute(query)).scalars().all()
