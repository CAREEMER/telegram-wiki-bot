from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot, dp
from models import User
from schemas.article import ArticleStatusEnum
from services._locale import Text, Texts
from services.article.get import list_articles
from services.language import get_primary_language
from services.utils import get_bot_link
from services.utils import sanitize_text as st


@dp.callback_query(lambda e: e.data.startswith("list_articles:"))
async def handle_list_articles(callback_query: CallbackQuery, user: User, session: AsyncSession):
    await callback_query.answer()
    page_size = 1

    _, page, new_message = callback_query.data.split(":")
    page = int(page)
    new_message = True if new_message == "1" else False

    excluded_article_statuses = []
    if user.is_default_user:
        excluded_article_statuses.append(ArticleStatusEnum.DELETED)

    articles = await list_articles(
        excluded_article_statuses=excluded_article_statuses,
        page=page,
        size=page_size,
        session=session,
    )

    bot_link = await get_bot_link()
    primary_language = await get_primary_language(session)

    text = Texts.get(Text.LIST_ARTICLES_MESSAGE) + "\n\n"
    for article in articles[:page_size]:
        if article.status == ArticleStatusEnum.DELETED:
            text += "🗑"

        article_title = article.get_title(user.language_id) or article.get_title(primary_language.id)
        text += f"[{st(article_title.content)}]({bot_link}?start=article_{article.id})\n\n"

    next_page, prev_page = page + 1, page - 1
    if page == 0 and len(articles) < page_size + 1:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=[])
    elif page == 0:
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=f">> {next_page + 1}", callback_data=f"list_articles:{next_page}:0")]
            ]
        )
    elif len(articles) < page_size + 1:
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=f"{prev_page + 1} <<", callback_data=f"list_articles:{prev_page}:0")],
            ]
        )
    else:
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=f"{prev_page + 1} <<", callback_data=f"list_articles:{prev_page}:0"
                    ),
                    types.InlineKeyboardButton(
                        text=f">> {next_page + 1}", callback_data=f"list_articles:{next_page}:0"
                    ),
                ]
            ]
        )

    if new_message:
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            reply_markup=reply_markup,
        )

    else:
        await bot.edit_message_text(
            chat_id=user.telegram_id,
            message_id=callback_query.message.message_id,
            text=text,
            reply_markup=reply_markup,
        )
