from sqlalchemy import BOOLEAN, VARCHAR, Column
from sqlalchemy.orm import Mapped

from core.db import DeclarativeBase
from models.base import BaseModelMixin


class Language(BaseModelMixin, DeclarativeBase):
    __tablename__ = "languages"

    emoji: Mapped[str] = Column(VARCHAR(255), nullable=False)
    code: Mapped[str] = Column(VARCHAR(255), nullable=False, unique=True, index=True)
    is_primary: Mapped[bool] = Column(BOOLEAN, server_default="f", nullable=False, index=True)
