from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update

from core.bot import dp
from core.db import async_session
from services._locale import ctx_language_var, primary_language_var
from services.language import get_language, get_primary_language
from services.user.get_or_create import get_or_create_user


@dp.update.outer_middleware()
async def register_user(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    update: Update,
    data: dict[str, Any],
):
    async with async_session() as session:
        data["user"] = await get_or_create_user(update.event.from_user, session)
        language = await get_language(data["user"].language_id, session) if data["user"].language_id else None
        primary_language = await get_primary_language(session)

    token = ctx_language_var.set(language.code if language else None)
    primary_token = primary_language_var.set(primary_language.code)

    await handler(update, data)

    ctx_language_var.reset(token)
    primary_language_var.reset(primary_token)
