"""Scheduler helpers for Nexon sync jobs."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.nexon.sync_service import NexonNoticeSyncService

class AppScheduler:
    """Entry point for manual or cron-driven sync jobs."""

    def __init__(self, db: Session) -> None:
        self._db = db

    async def sync_notice_events(self) -> dict[str, int]:
        service = NexonNoticeSyncService(self._db)
        saved, inserted, updated = await service.sync_notice_events()
        return {
            "total": len(saved),
            "inserted": inserted,
            "updated": updated,
        }

    async def sync_notice_event_detail(self, notice_id: int) -> int:
        service = NexonNoticeSyncService(self._db)
        saved = await service.sync_notice_event_detail(notice_id)
        return saved.notice_id
