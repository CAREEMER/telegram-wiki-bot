from sqlalchemy import (
    BIGINT,
    VARCHAR,
    Column,
    ForeignKey,
    LargeBinary,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, Relationship

from core.db import DeclarativeBase
from models.base import BaseModelMixin
from schemas.draft import DraftStatusEnum


class Draft(BaseModelMixin, DeclarativeBase):
    __tablename__ = "drafts"

    redactor_id: Mapped[int] = Column(BIGINT, ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[DraftStatusEnum] = Column(
        VARCHAR(255),
        server_default=DraftStatusEnum.CREATED,
        nullable=False,
        index=True,
    )
    origin_article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"))

    titles = Relationship("DraftTitle", back_populates="draft")
    texts = Relationship("DraftText", back_populates="draft")
    medias = Relationship("DraftMedia", back_populates="draft")

    def get_content(self, language_id: int) -> "tuple[DraftTitle | None, DraftText | None, DraftMedia | None]":
        return self.get_title(language_id), self.get_text(language_id), self.get_media(language_id)

    def get_title(self, language_id: int) -> "DraftTitle | None":
        if not self.titles:
            return None

        for title in self.titles:
            if title.language_id == language_id:
                return title

    def get_text(self, language_id: int) -> "DraftText | None":
        if not self.texts:
            return None

        for text in self.texts:
            if text.language_id == language_id:
                return text

    def get_media(self, language_id: int) -> "DraftMedia | None":
        if not self.medias:
            return None

        for media in self.medias:
            if media.language_id == language_id:
                return media


class DraftTitle(BaseModelMixin, DeclarativeBase):
    __tablename__ = "draft_titles"

    content: Mapped[str] = Column(VARCHAR(255), nullable=False, index=True)
    md_content: Mapped[str] = Column(Text, nullable=False)
    draft_id = Column(BIGINT, ForeignKey("drafts.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    draft = Relationship(Draft, back_populates="titles")

    __table_args__ = (UniqueConstraint("draft_id", "language_id"),)


class DraftText(BaseModelMixin, DeclarativeBase):
    __tablename__ = "draft_texts"

    content: Mapped[str] = Column(Text, nullable=False)
    md_content: Mapped[str] = Column(Text, nullable=False)
    draft_id = Column(BIGINT, ForeignKey("drafts.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    draft = Relationship(Draft, back_populates="texts")

    __table_args__ = (UniqueConstraint("draft_id", "language_id"),)


class DraftMedia(BaseModelMixin, DeclarativeBase):
    __tablename__ = "draft_medias"

    content: Mapped[bytes] = Column(LargeBinary, nullable=False)
    content_type: Mapped[str] = Column(VARCHAR(255), index=True, nullable=False)
    draft_id = Column(BIGINT, ForeignKey("drafts.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    draft = Relationship(Draft, back_populates="medias")

    __table_args__ = (UniqueConstraint("draft_id", "language_id"),)
