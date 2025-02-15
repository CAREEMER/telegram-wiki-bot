import enum


class ArticleStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class ReportStatusEnum(str, enum.Enum):
    CREATED = "created"
    RESOLVED = "resolved"
