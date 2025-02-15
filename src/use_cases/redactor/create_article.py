from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from services.draft.create import create_draft
from services.draft.editing_message import DraftEditingMessage
from services.draft.get import get_draft
from services.language import get_primary_language


async def create_blank_draft(redactor: User, session: AsyncSession) -> None:
    draft = await get_draft((await create_draft(redactor, session)).id, session)
    primary_language = await get_primary_language(session)

    await DraftEditingMessage(redactor, draft, primary_language, session).run()
