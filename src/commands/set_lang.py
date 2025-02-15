from aiogram import types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from services.user.get_or_create import get_user
from use_cases.start import show_initial_set_language_message, show_start_message
from use_cases.user import set_language_init


@dp.callback_query(lambda e: e.data.startswith("set_lang:"))
async def set_lang_callback_query_handler(callback_query: CallbackQuery, user: User, session: AsyncSession):
    await callback_query.answer()

    set_lang_id = int(callback_query.data.split(":")[1])
    await set_language_init(user.id, set_lang_id, session)
    user = await get_user(user_data=callback_query.from_user, session=session)
    await show_start_message(user, session)


@dp.message(Command("/lang"))
async def set_lang(message: types.Message, user: User, session: AsyncSession):
    await show_initial_set_language_message(user, session)
