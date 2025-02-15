from sqlalchemy import BIGINT, Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped

from core.db import DeclarativeBase
from models.base import BaseModelMixin


class Changelog(BaseModelMixin, DeclarativeBase):
    __tablename__ = "changelogs"

    redactor_id: Mapped[int] = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False, index=True)
    draft_id: Mapped[int] = Column(BIGINT, ForeignKey("drafts.id"), nullable=False)
    old_content: Mapped[dict] = Column(JSONB, nullable=False)
    new_content: Mapped[dict] = Column(JSONB, nullable=False)
