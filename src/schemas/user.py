import enum


class RoleEnum(str, enum.Enum):
    DEFAULT = "default"
    REDACTOR = "redactor"
    ADMIN = "admin"
