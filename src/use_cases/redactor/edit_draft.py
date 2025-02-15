from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from models import User
from services._locale import Text, Texts
from services.draft.content import (
    update_draft_content,
    update_draft_text,
    update_draft_title,
)
from services.draft.editing_message import DraftEditingMessage
from services.draft.get import get_draft
from services.language import get_language
from states.draft import EditDraftContentState


async def edit_draft_callback_init(
    draft_id: int, redactor: User, session: AsyncSession, state: FSMContext, args: list[str]
):
    draft = await get_draft(draft_id, session)

    method, *args = args

    if method == "lang":
        chosen_language_id = int(args[0])
        language = await get_language(chosen_language_id, session)

        return await DraftEditingMessage(
            redactor=redactor,
            draft=draft,
            language=language,
            session=session,
        ).run()

    user_state, message = None, None

    if method == "title":
        user_state = EditDraftContentState.title
        message = Texts.get(Text.UPDATE_DRAFT_TITLE_MESSAGE)
    elif method == "text":
        user_state = EditDraftContentState.text
        message = Texts.get(Text.UPDATE_DRAFT_TEXT_MESSAGE)
    elif method == "media":
        user_state = EditDraftContentState.media
        message = Texts.get(Text.UPDATE_DRAFT_MEDIA_MESSAGE)

    await state.set_state(user_state)
    await state.set_data(
        {
            "draft_id": draft_id,
            "language_id": int(args[0]),
        }
    )
    return await bot.send_message(
        chat_id=redactor.telegram_id,
        text=message,
    )


async def edit_draft_content(
    draft_id: int,
    language_id: int,
    redactor: User,
    session: AsyncSession,
    title_content: str | None = None,
    title_md_content: str | None = None,
    text_content: str | None = None,
    text_md_content: str | None = None,
    media_content: bytes | None = None,
    media_content_type: str | None = None,
):
    if title_content:
        await update_draft_title(
            draft_id=draft_id,
            language_id=language_id,
            content=title_content,
            md_content=title_md_content,
            session=session,
        )

    if text_content:
        await update_draft_text(
            draft_id=draft_id,
            language_id=language_id,
            content=text_content,
            md_content=text_md_content,
            session=session,
        )

    if media_content:
        await update_draft_content(
            draft_id=draft_id,
            language_id=language_id,
            content=media_content,
            content_type=media_content_type,
            session=session,
        )

    draft = await get_draft(draft_id=draft_id, session=session)
    language = await get_language(language_id=language_id, session=session)

    await DraftEditingMessage(
        redactor=redactor,
        draft=draft,
        language=language,
        session=session,
    ).run()
