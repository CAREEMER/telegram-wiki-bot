from sqlalchemy import (
    BIGINT,
    SMALLINT,
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
from schemas.article import ArticleStatusEnum, ReportStatusEnum


class Article(BaseModelMixin, DeclarativeBase):
    __tablename__ = "articles"

    status: Mapped[ArticleStatusEnum] = Column(
        VARCHAR(255), nullable=False, server_default=ArticleStatusEnum.ACTIVE, index=True
    )

    titles = Relationship("ArticleTitle", back_populates="article")
    texts = Relationship("ArticleText", back_populates="article")
    medias = Relationship("ArticleMedia", back_populates="article")

    def get_content(
        self, preferred_language_id: int, primary_language_id: int
    ) -> "tuple[ArticleTitle | None, ArticleText | None, ArticleMedia | None]":
        return (
            self.get_title(preferred_language_id) or self.get_title(primary_language_id),
            self.get_text(preferred_language_id) or self.get_text(primary_language_id),
            self.get_media(preferred_language_id) or self.get_media(primary_language_id),
        )

    def get_title(self, language_id: int) -> "ArticleTitle | None":
        if not self.titles:
            return None

        for title in self.titles:
            if title.language_id == language_id:
                return title

    def get_text(self, language_id: int) -> "ArticleText | None":
        if not self.texts:
            return None

        for text in self.texts:
            if text.language_id == language_id:
                return text

    def get_media(self, language_id: int) -> "ArticleMedia | None":
        if not self.medias:
            return None

        for media in self.medias:
            if media.language_id == language_id:
                return media


class ArticleTitle(BaseModelMixin, DeclarativeBase):
    __tablename__ = "article_titles"

    content: Mapped[str] = Column(VARCHAR(255), index=True, nullable=False)
    md_content: Mapped[str] = Column(Text, nullable=False)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    article = Relationship(Article, back_populates="titles")

    __table_args__ = (UniqueConstraint("article_id", "language_id"),)


class ArticleText(BaseModelMixin, DeclarativeBase):
    __tablename__ = "article_texts"

    content: Mapped[str] = Column(Text, nullable=False)
    md_content: Mapped[str] = Column(Text, nullable=False)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    article = Relationship(Article, back_populates="texts")

    __table_args__ = (UniqueConstraint("article_id", "language_id"),)


class ArticleMedia(BaseModelMixin, DeclarativeBase):
    __tablename__ = "article_medias"

    content: Mapped[bytes] = Column(LargeBinary, nullable=False)
    content_type: Mapped[str] = Column(VARCHAR(255), index=True, nullable=False)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False, index=True)
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)

    article = Relationship(Article, back_populates="medias")

    __table_args__ = (UniqueConstraint("article_id", "language_id"),)


class Report(BaseModelMixin, DeclarativeBase):
    __tablename__ = "reports"

    message: Mapped[str] = Column(VARCHAR(255))
    status: Mapped[ReportStatusEnum] = Column(
        VARCHAR(255), server_default=ReportStatusEnum.CREATED, nullable=False, index=True
    )
    language_id: Mapped[int] = Column(BIGINT, ForeignKey("languages.id"), nullable=False, index=True)
    reporter_id: Mapped[int] = Column(BIGINT, ForeignKey("users.id"), nullable=False, index=True)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False, index=True)


class MainArticle(BaseModelMixin, DeclarativeBase):
    __tablename__ = "main_articles"

    order_by: Mapped[int] = Column(SMALLINT, nullable=False)
    article_id: Mapped[int] = Column(BIGINT, ForeignKey("articles.id"), nullable=False)
