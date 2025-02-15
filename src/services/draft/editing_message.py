from aiogram import types
from aiogram.types import BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot import bot
from models import Draft, DraftMedia, DraftText, DraftTitle, Language, User
from services._locale import Text, Texts
from services.language import list_languages


class DraftEditingMessage:
    def __init__(self, redactor: User, draft: Draft, language: Language, session: AsyncSession) -> None:
        self.redactor: User = redactor
        self.draft: Draft = draft
        self.language: Language = language
        self.session: AsyncSession = session

    async def get_draft_content(self) -> tuple[DraftTitle | None, DraftText | None, DraftMedia | None]:
        return self.draft.get_content(self.language.id)

    async def construct_message_text(self, title: DraftTitle, text: DraftText, media: DraftMedia) -> str:
        text = (
            f"Draft ID\\: {self.draft.id}\n\nLanguage\\: {self.language.emoji}\n\n"
            + ("" if media else "Media\\: none\n\n")
            + (f"{title.md_content}\n\n" if title else "Title\\: none\n\n")
            + (f"{text.md_content}\n\n" if text else "Text\\: none\n\n")
        )
        if self.draft.origin_article_id:
            text = f"Article ID\\: {self.draft.origin_article_id}\n" + text

        return text

    async def construct_inline_keyboard(self) -> types.InlineKeyboardMarkup:
        inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

        languages = await list_languages(self.session)
        inline_keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=lang.emoji, callback_data=f"edit_draft_content:{self.draft.id}:lang:{lang.id}"
                )
                for lang in languages
            ]
        )

        inline_keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=Texts.get(Text.EDIT_DRAFT_TITLE_BUTTON),
                    callback_data=f"edit_draft_content:{self.draft.id}:title:{self.language.id}",
                ),
            ]
        )

        inline_keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=Texts.get(Text.EDIT_DRAFT_TEXT_BUTTON),
                    callback_data=f"edit_draft_content:{self.draft.id}:text:{self.language.id}",
                ),
            ]
        )

        inline_keyboard.inline_keyboard.append(
            [
                types.InlineKeyboardButton(
                    text=Texts.get(Text.EDIT_DRAFT_MEDIA_BUTTON),
                    callback_data=f"edit_draft_content:{self.draft.id}:media:{self.language.id}",
                ),
            ]
        )

        save_button_text = (
            Texts.get(Text.SAVE_DRAFT_BUTTON) if self.draft.origin_article_id else Texts.get(Text.SUBMIT_DRAFT_BUTTON)
        )
        inline_keyboard.inline_keyboard.append(
            [types.InlineKeyboardButton(text=save_button_text, callback_data=f"submit_draft:{self.draft.id}")]
        )

        return inline_keyboard

    async def run(self):
        title, text, media = await self.get_draft_content()

        message = await self.construct_message_text(title, text, media)
        reply_markup = await self.construct_inline_keyboard()

        if not media:
            return await bot.send_message(
                chat_id=self.redactor.telegram_id,
                text=message,
                reply_markup=reply_markup,
            )

        if media.content_type == types.ContentType.ANIMATION:
            return await bot.send_animation(
                chat_id=self.redactor.telegram_id,
                animation=BufferedInputFile(media.content, filename="animation.gif"),
                caption=message,
                reply_markup=reply_markup,
            )

        elif media.content_type == types.ContentType.PHOTO:
            await bot.send_photo(
                chat_id=self.redactor.telegram_id,
                photo=BufferedInputFile(media.content, filename="article_image.png"),
                caption=message,
                reply_markup=reply_markup,
            )

        elif media.content_type == types.ContentType.VIDEO:
            await bot.send_video(
                chat_id=self.redactor.telegram_id,
                video=BufferedInputFile(media.content, filename="video.mp4"),
                caption=message,
                reply_markup=reply_markup,
            )
