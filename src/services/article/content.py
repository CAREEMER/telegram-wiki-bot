from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import ArticleMedia, ArticleText, ArticleTitle, Draft


async def create_content_from_draft(draft: Draft, article_id: int, session: AsyncSession) -> None:
    title_contents, text_contents, media_contents = [], [], []

    for title in draft.titles or []:
        title_contents.append(
            {
                "article_id": article_id,
                "content": title.content,
                "md_content": title.md_content,
                "language_id": title.language_id,
            }
        )

    for text in draft.texts or []:
        text_contents.append(
            {
                "article_id": article_id,
                "content": text.content,
                "md_content": text.md_content,
                "language_id": text.language_id,
            }
        )

    for media in draft.medias or []:
        media_contents.append(
            {
                "article_id": article_id,
                "content": media.content,
                "content_type": media.content_type,
                "language_id": media.language_id,
            }
        )

    await session.execute(delete(ArticleTitle).where(ArticleTitle.article_id == article_id))
    await session.execute(delete(ArticleText).where(ArticleText.article_id == article_id))
    await session.execute(delete(ArticleMedia).where(ArticleMedia.article_id == article_id))

    if title_contents:
        await session.execute(insert(ArticleTitle).values(title_contents))
    if text_contents:
        await session.execute(insert(ArticleText).values(text_contents))
    if media_contents:
        await session.execute(insert(ArticleMedia).values(media_contents))
