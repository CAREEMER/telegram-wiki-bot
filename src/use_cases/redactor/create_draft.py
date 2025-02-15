from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from services.article.get import get_article
from services.draft.content import create_content_from_article
from services.draft.create import create_draft
from services.draft.editing_message import DraftEditingMessage
from services.draft.get import get_draft
from services.language import get_primary_language


async def create_draft_from_article(
    article_id: int,
    redactor: User,
    session: AsyncSession,
):
    article = await get_article(article_id, session)
    draft = await create_draft(redactor, session, origin_article_id=article.id)

    await create_content_from_article(
        article=article,
        draft_id=draft.id,
        session=session,
    )

    draft = await get_draft(draft.id, session)
    primary_language = await get_primary_language(session)

    await DraftEditingMessage(
        redactor=redactor,
        draft=draft,
        language=primary_language,
        session=session,
    ).run()
