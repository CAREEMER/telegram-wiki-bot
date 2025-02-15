from datetime import datetime

from sqlalchemy import BIGINT, Column, DateTime, func
from sqlalchemy.orm import Mapped


class IDMixin:
    id: Mapped[int] = Column(BIGINT, primary_key=True, autoincrement=True)


class TimeStampMixin:
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class BaseModelMixin(IDMixin, TimeStampMixin):
    pass
