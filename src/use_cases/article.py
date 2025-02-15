from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.article import ArticleStatusEnum
from services._locale import Text, Texts
from services.article.message import show_article_message
from services.article.search import perform_article_search
from services.language import get_primary_language
from services.utils import get_bot_link


async def open_article_message(message: types.Message, user: User, session: AsyncSession):
    article_id = message.text.split(" ")[-1].split("_")[-1]
    await show_article_message(
        article_id=int(article_id),
        user=user,
        session=session,
    )


async def search_articles(message: types.Message, user: User, session: AsyncSession):
    tokens = message.text.replace("/search ", "").split(" ")

    exclude_article_statuses = []
    if user.is_default_user:
        exclude_article_statuses.append(ArticleStatusEnum.DELETED)

    articles = await perform_article_search(tokens, exclude_article_statuses, session)

    if not articles:
        return await message.reply(
            text=Texts.get(Text.ERROR_NO_ARTICLES_FOUND),
        )

    text = Texts.get(Text.SEARCH_ARTICLES_MESSAGE) + "\n\n"
    bot_link = await get_bot_link()

    primary_language = await get_primary_language(session)

    for article in articles:
        article_link = f"{bot_link}?start=article_{article.id}"

        article_title = article.get_title(user.language_id) or article.get_title(primary_language.id)
        text += f"[{article_title.content}]({article_link})\n\n"

    await message.reply(text=text)
