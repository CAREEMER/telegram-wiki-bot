from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from use_cases.redactor.create_article import create_blank_draft


@dp.callback_query(lambda e: e.data.startswith("create_article:"))
async def create_article_callback_query_handler(callback_query: types.CallbackQuery, user: User, session: AsyncSession):
    await callback_query.answer()
    await create_blank_draft(redactor=user, session=session)
