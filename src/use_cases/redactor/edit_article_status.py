from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from models import User
from schemas.article import ArticleStatusEnum
from services.article.get import get_article
from services.article.message import show_article_message
from services.article.update import update_article


async def edit_article_status(article_id: int, redactor: User, session: AsyncSession) -> None:
    article = await get_article(article_id, session)

    reply_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=row.name, callback_data=f"set_article_status:{article_id}:{row.value}")]
            for row in ArticleStatusEnum
        ]
    )

    await bot.send_message(
        chat_id=redactor.telegram_id,
        text=f"Article ID: {article_id}\n\nCurrent status: {article.status}",
        reply_markup=reply_markup,
    )


async def set_article_status(
    article_id: int, new_status: ArticleStatusEnum, redactor: User, session: AsyncSession
) -> None:
    await update_article(article_id, session, status=new_status)

    await show_article_message(article_id, redactor, session)
