from aiogram import types
from aiogram.types import BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from models import User
from schemas.article import ArticleStatusEnum
from services._locale import Text, Texts
from services.article.get import get_article
from services.language import get_primary_language
from services.utils import get_bot_link


async def show_article_message(article_id: int, user: User, session: AsyncSession):
    article = await get_article(article_id, session)

    if user.is_default_user and article.status == ArticleStatusEnum.DELETED:
        return await bot.send_message(
            chat_id=user.telegram_id,
            text=Texts.get(Text.ERROR_DELETED_ARTICLE_MESSAGE),
        )

    primary_language = await get_primary_language(session)
    title, text, media = article.get_content(user.language_id, primary_language.id)

    bot_link = await get_bot_link()
    article_link = f"{bot_link}?start=article_{article_id}"

    text = f"{title.md_content}\n\n{text.md_content}\n\n[" + Texts.get(Text.SHARE_ARTICLE_TEXT) + f"]({article_link})"

    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[])

    if user.is_redactor:
        reply_markup.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=Texts.get(Text.CHANGE_ARTICLE_STATUS_BUTTON), callback_data=f"edit_article_status:{article_id}"
                )
            ]
        )
        reply_markup.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=Texts.get(Text.EDIT_ARTICLE_CONTENT_BUTTON), callback_data=f"edit_article:{article_id}"
                )
            ]
        )

    if not media:
        return await bot.send_message(
            chat_id=user.telegram_id, text=text, reply_markup=reply_markup, disable_web_page_preview=True
        )

    if media.content_type == types.ContentType.PHOTO:
        await bot.send_photo(
            chat_id=user.telegram_id,
            photo=BufferedInputFile(media.content, filename="article_image.png"),
            caption=text,
            reply_markup=reply_markup,
        )
    elif media.content_type == types.ContentType.VIDEO:
        await bot.send_video(
            chat_id=user.telegram_id,
            video=BufferedInputFile(media.content, filename="article_video.mp4"),
            caption=text,
            reply_markup=reply_markup,
        )
    elif media.content_type == types.ContentType.ANIMATION:
        await bot.send_animation(
            chat_id=user.telegram_id,
            animation=BufferedInputFile(media.content, filename="article_animation.gif"),
            caption=text,
            reply_markup=reply_markup,
        )
