from core.bot import bot
from services.cache import CacheService


def sanitize_text(text: str):
    escape_chars = ["_", ".", "-", "#", "(", ")", "[", "]", "!", "*", ">", "<", "`", "~", "|", "="]
    for char in escape_chars:
        text = text.replace(char, "\\" + char)

    return text


async def get_bot_link() -> str:
    cache_key = "bot_link"
    bot_link = await CacheService.get_data(key=cache_key)
    if bot_link:
        return bot_link

    me = await bot.get_me()
    bot_link = f"https://t.me/{me.username}"
    await CacheService.set_data(key=cache_key, value=bot_link)

    return bot_link
