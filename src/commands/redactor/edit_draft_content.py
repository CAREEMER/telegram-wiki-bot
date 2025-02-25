import io

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot, dp
from exceptions.draft_edit import DraftTooLongTextException, DraftTooLongTitleException
from models import User
from services._locale import Text, Texts
from states.draft import EditDraftContentState
from use_cases.redactor.edit_draft import (
    edit_draft_callback_init,
    edit_draft_content,
    validate_text_content,
    validate_title_content,
)


@dp.callback_query(lambda e: e.data.startswith("edit_draft_content:"))
async def edit_draft_content_callback_query(
    callback_query: types.CallbackQuery, user: User, session: AsyncSession, state: FSMContext
):
    await callback_query.answer()
    await state.clear()

    _, draft_id, *args = callback_query.data.split(":")
    draft_id = int(draft_id)

    await edit_draft_callback_init(draft_id=draft_id, redactor=user, session=session, state=state, args=args)


@dp.message(EditDraftContentState.title)
async def edit_draft_title(message: types.Message, state: FSMContext, user: User, session: AsyncSession):
    state_data = await state.get_data()

    try:
        await validate_title_content(content=message.text)
    except DraftTooLongTitleException as e:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=Texts.get(Text.ERROR_TOO_LONG_DRAFT_TITLE).format(
                content_length=e.length,
                max_content_length=e.max_length,
            ),
        )
        return

    await state.clear()

    await edit_draft_content(
        draft_id=state_data["draft_id"],
        language_id=state_data["language_id"],
        redactor=user,
        session=session,
        title_md_content=message.md_text,
        title_content=message.text,
    )


@dp.message(EditDraftContentState.text)
async def edit_draft_text(message: types.Message, state: FSMContext, user: User, session: AsyncSession):
    state_data = await state.get_data()

    try:
        await validate_text_content(content=message.text)
    except DraftTooLongTextException as e:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=Texts.get(Text.ERROR_TOO_LONG_DRAFT_TEXT).format(
                content_length=e.length,
                max_content_length=e.max_length,
            ),
        )
        return

    await state.clear()

    await edit_draft_content(
        draft_id=state_data["draft_id"],
        language_id=state_data["language_id"],
        redactor=user,
        session=session,
        text_md_content=message.md_text,
        text_content=message.text,
    )


@dp.message(EditDraftContentState.media)
async def edit_draft_media(message: types.Message, state: FSMContext, user: User, session: AsyncSession):
    if message.content_type not in (
        types.ContentType.PHOTO,
        types.ContentType.ANIMATION,
        types.ContentType.VIDEO,
    ):
        return

    state_data = await state.get_data()
    await state.clear()

    file_id = None

    if message.content_type == types.ContentType.ANIMATION:
        file_id = message.animation.file_id

    elif message.content_type == types.ContentType.PHOTO:
        file_id = message.photo[-1].file_id

    elif message.content_type == types.ContentType.VIDEO:
        file_id = message.video.file_id

    file = await bot.get_file(file_id)
    photo_buffer = io.BytesIO()
    await bot.download_file(file.file_path, photo_buffer)
    photo_buffer.seek(0)

    await edit_draft_content(
        draft_id=state_data["draft_id"],
        language_id=state_data["language_id"],
        redactor=user,
        session=session,
        media_content=photo_buffer.read(),
        media_content_type=message.content_type.value,
    )
