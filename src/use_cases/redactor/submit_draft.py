from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from exceptions.draft_submit import (
    DraftAlreadyPublishedException,
    DraftNoPrimaryLanguageException,
)
from models import Draft, User
from schemas.draft import DraftStatusEnum
from services._locale import Text, Texts
from services.article.create import (
    create_article_from_draft,
    update_article_content_from_draft,
)
from services.article.message import show_article_message
from services.draft.get import get_draft
from services.language import get_primary_language


async def validate_draft(draft: Draft, session: AsyncSession):
    primary_language = await get_primary_language(session)

    if not all((draft.get_title(primary_language.id), draft.get_text(primary_language.id))):
        raise DraftNoPrimaryLanguageException(
            language_code=primary_language.code, language_emoji=primary_language.emoji
        )

    if draft.status != DraftStatusEnum.CREATED:
        raise DraftAlreadyPublishedException


async def submit_draft(draft_id: int, redactor: User, session: AsyncSession) -> None:
    draft = await get_draft(draft_id=draft_id, session=session)

    try:
        await validate_draft(draft, session)
    except DraftNoPrimaryLanguageException as e:
        return await bot.send_message(
            chat_id=redactor.telegram_id,
            text=Texts.get(Text.ERROR_DRAFT_NO_PRIMARY_LANGUAGE_CONTENT).format(
                language_emoji=e.language_emoji, language_code=e.language_code
            ),
        )
    except DraftAlreadyPublishedException:
        return await bot.send_message(chat_id=redactor.telegram_id, text=Texts.get(Text.ERROR_DRAFT_ALREADY_SUBMITTED))

    if draft.origin_article_id:
        article_id = draft.origin_article_id
        await update_article_content_from_draft(draft, article_id, session)

    else:
        article_id = await create_article_from_draft(draft, session)

    await show_article_message(article_id, redactor, session)
