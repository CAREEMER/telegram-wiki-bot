import enum
import json
from contextvars import ContextVar

ctx_language_var = ContextVar("language_id")
primary_language_var = ContextVar("primary_language")


class Text(str, enum.Enum):
    # MESSAGES
    START_MESSAGE = "start_message"
    INITIAL_CHOOSE_LANGUAGE_MESSAGE = "initial_choose_language_message"
    SEARCH_ARTICLES_MESSAGE = "search_articles_message"
    LIST_ARTICLES_MESSAGE = "list_articles_message"
    SHARE_ARTICLE_TEXT = "share_article_text"

    # DEFAULT USERS
    LIST_ARTICLES_BUTTON = "list_articles_button"

    # REDACTORS
    CREATE_ARTICLE_BUTTON = "create_article_button"
    CHANGE_ARTICLE_STATUS_BUTTON = "change_article_status_button"
    EDIT_ARTICLE_CONTENT_BUTTON = "edit_article_content_button"
    EDIT_DRAFT_TITLE_BUTTON = "edit_draft_title_button"
    EDIT_DRAFT_TEXT_BUTTON = "edit_draft_text_button"
    EDIT_DRAFT_MEDIA_BUTTON = "edit_draft_media_button"
    SUBMIT_DRAFT_BUTTON = "submit_draft_button"
    SAVE_DRAFT_BUTTON = "save_draft_button"
    UPDATE_DRAFT_TITLE_MESSAGE = "update_draft_title_message"
    UPDATE_DRAFT_TEXT_MESSAGE = "update_draft_text_message"
    UPDATE_DRAFT_MEDIA_MESSAGE = "update_draft_media_message"

    # ERRORS
    ERROR_DELETED_ARTICLE_MESSAGE = "error_deleted_article_message"
    ERROR_NO_ARTICLES_FOUND = "error_no_articles_found"
    ERROR_DRAFT_NO_PRIMARY_LANGUAGE_CONTENT = "error_draft_no_primary_language_content"
    ERROR_DRAFT_ALREADY_SUBMITTED = "error_draft_already_submitted"
    ERROR_TOO_LONG_DRAFT_TITLE = "error_too_long_draft_title"
    ERROR_TOO_LONG_DRAFT_TEXT = "error_too_long_draft_text"


def load_locale() -> None:
    with open("locale.json", "r") as locale_file:
        return json.load(locale_file)


class Texts:
    locale_json: dict | None = None

    @classmethod
    def get(cls, _text: Text, language_code: str | None = None) -> str:
        if not cls.locale_json:
            cls.locale_json = load_locale()

        ctx_language_code = language_code or ctx_language_var.get()
        primary_language_code = primary_language_var.get()

        return cls.locale_json.get(_text).get(
            ctx_language_code,
            cls.locale_json.get(_text).get(primary_language_code),
        )
