"""Example ORM model for Nexon MapleStory event notices."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NexonNoticeEvent(Base):
    """Example table for storing Nexon event notices."""

    __tablename__ = "nexon_notice_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notice_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    notice_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    event_start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    event_end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    contents: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    raw_payload: Mapped[str] = mapped_column(String, nullable=False)
