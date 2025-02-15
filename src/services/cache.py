from redis.asyncio import Redis

from core.settings import settings

redis_client = Redis.from_url(settings.REDIS_DSN)


class CacheService:
    @classmethod
    async def get_data(cls, key: str) -> str | None:
        result = await redis_client.get(key)

        if result:
            return result.decode()

    @classmethod
    async def set_data(cls, key: str, value: str, ex: int | None = None):
        await redis_client.set(key, value.encode(), ex=ex)
