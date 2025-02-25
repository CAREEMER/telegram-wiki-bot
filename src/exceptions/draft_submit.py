class DraftSubmitException(Exception):
    pass


class DraftNoPrimaryLanguageException(DraftSubmitException):
    def __init__(self, language_code: str, language_emoji: str):
        self.language_code = language_code
        self.language_emoji = language_emoji


class DraftAlreadyPublishedException(DraftSubmitException):
    pass
