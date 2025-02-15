from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update

from core.bot import dp
from core.db import async_session


@dp.update.outer_middleware()
async def get_db_session(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    update: Update,
    data: dict[str, Any],
):
    async with async_session() as session:
        data["session"] = session
        await handler(update, data)
