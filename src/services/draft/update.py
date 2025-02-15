from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Draft
from schemas.draft import DraftStatusEnum


async def update_draft(draft_id: int, status: DraftStatusEnum, session: AsyncSession) -> None:
    query = update(Draft).where(Draft.id == draft_id).values(status=status)
    await session.execute(query)
