from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from models import User
from services._locale import Text, Texts
from services.article.get import get_main_articles
from services.language import get_primary_language, list_languages
from services.utils import get_bot_link


async def show_initial_set_language_message(
    user: User,
    session: AsyncSession,
) -> None:
    available_languages = await list_languages(session)

    await bot.send_message(
        chat_id=user.telegram_id,
        text=Texts.get(Text.INITIAL_CHOOSE_LANGUAGE_MESSAGE),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=f"{lang.emoji} {lang.code.upper()}", callback_data=f"set_lang:{lang.id}"
                    )
                ]
                for lang in available_languages
            ]
        ),
    )


async def show_start_message(user: User, session: AsyncSession):
    if not user.language_id:
        return await show_initial_set_language_message(user, session)

    reply_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Texts.get(Text.LIST_ARTICLES_BUTTON), callback_data="list_articles:0:1")]
        ]
    )

    if user.is_redactor:
        reply_markup.inline_keyboard.append(
            [types.InlineKeyboardButton(text=Texts.get(Text.CREATE_ARTICLE_BUTTON), callback_data="create_article:")]
        )

    primary_language = await get_primary_language(session)
    main_articles = await get_main_articles(session)

    message_text = Texts.get(Text.START_MESSAGE) + "\n\n"

    bot_link = await get_bot_link()

    for main_article in main_articles:
        title = main_article.get_title(user.language_id) or main_article.get_title(primary_language.id)
        message_text += f"[{title.md_content}]({bot_link}?start=article_{main_article.id})\n\n"

    await bot.send_message(
        chat_id=user.telegram_id,
        text=message_text,
        reply_markup=reply_markup,
    )
