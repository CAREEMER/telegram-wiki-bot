from core.settings import settings


class DraftEditException(Exception):
    pass


class DraftTooLongTitleException(DraftEditException):
    def __init__(
        self,
        length: int,
        max_length: int = settings.TITLE_CONTENT_LENGTH,
    ):
        self.length = length
        self.max_length = max_length


class DraftTooLongTextException(DraftEditException):
    def __init__(
        self,
        length: int,
        max_length: int = settings.TEXT_CONTENT_LENGTH,
    ):
        self.length = length
        self.max_length = max_length
