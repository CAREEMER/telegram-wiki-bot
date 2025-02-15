from sqlalchemy import BIGINT, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import Mapped

from core.db import DeclarativeBase
from models.base import BaseModelMixin
from schemas.user import RoleEnum


class User(BaseModelMixin, DeclarativeBase):
    __tablename__ = "users"

    telegram_id: Mapped[str] = Column(VARCHAR(255), nullable=False, index=True, unique=True)
    username: Mapped[str | None] = Column(VARCHAR(255))
    mention: Mapped[str | None] = Column(VARCHAR(255))
    full_name: Mapped[str | None] = Column(VARCHAR(255))
    role: Mapped[RoleEnum] = Column(VARCHAR(255), server_default=RoleEnum.DEFAULT)
    language_id: Mapped[int | None] = Column(BIGINT, ForeignKey("languages.id"))

    @property
    def is_default_user(self) -> bool:
        return self.role == RoleEnum.DEFAULT

    @property
    def is_redactor(self) -> bool:
        return self.role in (RoleEnum.REDACTOR, RoleEnum.ADMIN)

    @property
    def is_admin(self) -> bool:
        return self.role == RoleEnum.ADMIN
