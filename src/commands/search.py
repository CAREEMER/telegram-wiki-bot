from aiogram import types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from use_cases.article import search_articles


@dp.message(Command("search"))
async def handler_search_articles(message: types.Message, user: User, session: AsyncSession):
    await search_articles(message, user, session)
