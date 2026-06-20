"""Schemas for Nexon MapleStory event notices."""

from __future__ import annotations

from datetime import datetime

from app.schemas.base import SchemaBase


class NexonNoticeEventItem(SchemaBase):
    title: str
    url: str
    notice_id: int
    date: datetime
    date_event_start: datetime | None = None
    date_event_end: datetime | None = None


class NexonNoticeEventResponse(SchemaBase):
    event_notice: list[NexonNoticeEventItem]


class NexonNoticeEventDetailResponse(SchemaBase):
    title: str
    url: str
    contents: str
    date: datetime
    date_event_start: datetime | None = None
    date_event_end: datetime | None = None


class NexonNoticeSyncResponse(SchemaBase):
    total: int
    inserted: int
    updated: int
    notices: list[NexonNoticeEventItem]
