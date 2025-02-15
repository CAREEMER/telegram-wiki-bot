import enum


class DraftStatusEnum(str, enum.Enum):
    CREATED = "created"
    DEPLOYED = "deployed"
