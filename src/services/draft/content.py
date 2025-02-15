from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Article, DraftMedia, DraftText, DraftTitle


async def update_draft_title(draft_id: int, language_id: int, content: str, md_content: str, session: AsyncSession):
    query = (
        pg_insert(DraftTitle)
        .values(
            content=content,
            md_content=md_content,
            draft_id=draft_id,
            language_id=language_id,
        )
        .on_conflict_do_update(
            index_elements=["draft_id", "language_id"],
            set_={"content": content, "md_content": md_content},
        )
    )

    await session.execute(query)


async def update_draft_text(draft_id: int, language_id: int, content: str, md_content: str, session: AsyncSession):
    query = (
        pg_insert(DraftText)
        .values(
            content=content,
            md_content=md_content,
            draft_id=draft_id,
            language_id=language_id,
        )
        .on_conflict_do_update(
            index_elements=["draft_id", "language_id"],
            set_={"content": content, "md_content": md_content},
        )
    )

    await session.execute(query)


async def update_draft_content(
    draft_id: int, language_id: int, content: bytes, content_type: str, session: AsyncSession
):
    query = (
        pg_insert(DraftMedia)
        .values(
            content=content,
            content_type=content_type,
            draft_id=draft_id,
            language_id=language_id,
        )
        .on_conflict_do_update(
            index_elements=["draft_id", "language_id"],
            set_={"content": content, "content_type": content_type},
        )
    )

    await session.execute(query)


async def create_content_from_article(article: Article, draft_id: int, session: AsyncSession) -> None:
    title_contents, text_contents, media_contents = [], [], []

    for title in article.titles or []:
        title_contents.append(
            {
                "draft_id": draft_id,
                "content": title.content,
                "md_content": title.md_content,
                "language_id": title.language_id,
            }
        )

    for text in article.texts or []:
        text_contents.append(
            {
                "draft_id": draft_id,
                "content": text.content,
                "md_content": text.md_content,
                "language_id": text.language_id,
            }
        )

    for media in article.medias or []:
        media_contents.append(
            {
                "draft_id": draft_id,
                "content": media.content,
                "content_type": media.content_type,
                "language_id": media.language_id,
            }
        )

    if title_contents:
        await session.execute(insert(DraftTitle).values(title_contents))
    if text_contents:
        await session.execute(insert(DraftText).values(text_contents))
    if media_contents:
        await session.execute(insert(DraftMedia).values(media_contents))
