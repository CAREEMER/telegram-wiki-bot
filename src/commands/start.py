from aiogram import types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from use_cases.article import open_article_message
from use_cases.start import show_start_message


async def route_start_subcommand(message: types.Message, user: User, session: AsyncSession) -> None:
    subcommand = message.text.split(" ")[1].split("_")[0]

    subcommand_router_map = {
        "article": open_article_message,
    }
    return await subcommand_router_map[subcommand](message, user, session)


@dp.message(CommandStart())
async def process_start_command(message: types.Message, user: User, session: AsyncSession) -> None:
    if message.text != "/start":
        return await route_start_subcommand(message, user, session)

    return await show_start_message(user, session)
