import httpx

from core.settings import settings


async def upload(file_name: str):
    headers = {
        # "User-Agent": "DiscordBot (Discord.py, 1.0.0)",
        "Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}"
    }
    url = f"https://discord.com/api/v10/channels/{settings.DISCORD_CDN_CHAT_ID}/messages"
    data = {"file": open(file_name, "rb")}
    r = httpx.post(url, headers=headers, files=data)
    return r.json()["attachments"][0]["url"]
