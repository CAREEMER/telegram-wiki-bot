from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import dp
from models import User
from use_cases.redactor.submit_draft import submit_draft


@dp.callback_query(lambda e: e.data.startswith("submit_draft:"))
async def submit_draft_query(callback_query: CallbackQuery, user: User, session: AsyncSession):
    await callback_query.answer()
    _, draft_id = callback_query.data.split(":")
    draft_id = int(draft_id)

    await submit_draft(
        draft_id=draft_id,
        redactor=user,
        session=session,
    )
