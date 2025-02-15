from aiogram.fsm.state import State, StatesGroup


class EditDraftContentState(StatesGroup):
    draft_id: int = State()
    language_id: int = State()
    title: str = State()
    text: str = State()
    media: str = State()
