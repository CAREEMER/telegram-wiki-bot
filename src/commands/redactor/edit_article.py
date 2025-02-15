from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from use_cases.redactor.create_draft import create_draft_from_article
from use_cases.redactor.edit_article_status import (
    edit_article_status,
    set_article_status,
)


@dp.callback_query(lambda e: e.data.startswith("edit_article:"))
async def handle_edit_article(callback: CallbackQuery, user: User, session: AsyncSession):
    await callback.answer()
    article_id = int(callback.data.split(":")[-1])

    await create_draft_from_article(
        article_id=article_id,
        redactor=user,
        session=session,
    )


@dp.callback_query(lambda e: e.data.startswith("edit_article_status:"))
async def handle_edit_article_status(callback: CallbackQuery, user: User, session: AsyncSession):
    await callback.answer()
    article_id = int(callback.data.split(":")[-1])

    await edit_article_status(
        article_id=article_id,
        redactor=user,
        session=session,
    )


@dp.callback_query(lambda e: e.data.startswith("set_article_status:"))
async def handle_set_article_status(callback: CallbackQuery, user: User, session: AsyncSession):
    await callback.answer()
    _, article_id, new_status = callback.data.split(":")
    article_id = int(article_id)

    await set_article_status(
        article_id=article_id,
        new_status=new_status,
        redactor=user,
        session=session,
    )
