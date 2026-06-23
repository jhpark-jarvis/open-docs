"""Service for syncing Nexon notices into the database."""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.nexon_notice import NexonNoticeEvent
from app.services.nexon.client import NexonNoticeEvent as NexonNoticeEventDTO
from app.services.nexon.client import NexonNoticeEventDetail
from app.services.nexon.client import NexonOpenApiClient


class NexonNoticeSyncService:
    """Orchestration layer for notice synchronization."""

    _KST = ZoneInfo("Asia/Seoul")

    def __init__(self, db: Session, client: NexonOpenApiClient | None = None) -> None:
        # DB 세션과 Nexon API 클라이언트를 주입받아 재사용 가능한 서비스로 둡니다.
        self._db = db
        self._client = client or NexonOpenApiClient()

    async def sync_notice_events(self) -> tuple[list[NexonNoticeEvent], int, int]:
        # 목록 API를 호출한 뒤, 신규/변경 건만 상세까지 함께 동기화합니다.
        notice_events = await self._client.fetch_notice_events()
        return await self._sync_notice_events_with_details(notice_events)

    async def _sync_notice_events_with_details(
        self, notice_events: Sequence[NexonNoticeEventDTO]
    ) -> tuple[list[NexonNoticeEvent], int, int]:
        # 목록 메타와 상세 본문을 함께 맞추되, detail 조회가 필요한 항목만 호출합니다.
        saved: list[NexonNoticeEvent] = []
        inserted = 0
        updated = 0

        for item in notice_events:
            # notice_id 기준으로 기존 레코드를 찾습니다.
            instance = (
                self._db.query(NexonNoticeEvent)
                .filter(NexonNoticeEvent.notice_id == item.notice_id)
                .one_or_none()
            )

            if self._requires_detail_sync(instance, item):
                detail = await self._client.fetch_notice_event_detail(item.notice_id)
                instance, was_inserted = self._save_notice_event_detail(
                    notice_id=item.notice_id,
                    detail=detail,
                    instance=instance,
                )
            else:
                instance, was_inserted = self._save_notice_event_metadata(item, instance=instance)

            if was_inserted:
                inserted += 1
            else:
                updated += 1

            saved.append(instance)

        # 목록 응답에 없어진 기존 이벤트도 현재 시각 기준으로 활성 상태를 다시 계산합니다.
        self._refresh_active_flags()

        # 한 번에 commit해서 목록 sync를 하나의 단위 작업으로 처리합니다.
        self._db.commit()
        for instance in saved:
            self._db.refresh(instance)
        return saved, inserted, updated

    async def sync_notice_event_detail(self, notice_id: int) -> NexonNoticeEvent:
        # 상세 API를 호출해 본문(contents)까지 가져옵니다.
        detail = await self._client.fetch_notice_event_detail(notice_id)
        return self._upsert_notice_event_detail(notice_id, detail)

    def _upsert_notice_event_detail(
        self, notice_id: int, detail: NexonNoticeEventDetail
    ) -> NexonNoticeEvent:
        # 상세 저장도 목록과 동일하게 notice_id 기준으로 대상 레코드를 찾습니다.
        instance = (
            self._db.query(NexonNoticeEvent)
            .filter(NexonNoticeEvent.notice_id == notice_id)
            .one_or_none()
        )
        instance, _ = self._save_notice_event_detail(notice_id=notice_id, detail=detail, instance=instance)

        # 상세 동기화도 하나의 저장 단위로 commit합니다.
        self._db.commit()
        self._db.refresh(instance)
        return instance

    def _save_notice_event_metadata(
        self,
        item: NexonNoticeEventDTO,
        instance: NexonNoticeEvent | None = None,
    ) -> tuple[NexonNoticeEvent, bool]:
        payload = self._serialize_notice_payload(
            {
                "title": item.title,
                "url": item.url,
                "notice_id": item.notice_id,
                "date": item.date.isoformat(),
                "date_event_start": item.date_event_start.isoformat()
                if item.date_event_start
                else None,
                "date_event_end": item.date_event_end.isoformat() if item.date_event_end else None,
            }
        )
        is_active = self._is_active(item.date_event_start, item.date_event_end)
        was_inserted = instance is None

        if instance is None:
            instance = NexonNoticeEvent(
                notice_id=item.notice_id,
                title=item.title,
                url=item.url,
                notice_date=item.date,
                event_start_date=item.date_event_start,
                event_end_date=item.date_event_end,
                contents=None,
                is_active=is_active,
                raw_payload=payload,
            )
            self._db.add(instance)
        else:
            instance.title = item.title
            instance.url = item.url
            instance.notice_date = item.date
            instance.event_start_date = item.date_event_start
            instance.event_end_date = item.date_event_end
            instance.is_active = is_active
            instance.raw_payload = payload

        return instance, was_inserted

    def _save_notice_event_detail(
        self,
        notice_id: int,
        detail: NexonNoticeEventDetail,
        instance: NexonNoticeEvent | None = None,
    ) -> tuple[NexonNoticeEvent, bool]:
        payload = self._serialize_notice_payload(
            {
                "title": detail.title,
                "url": detail.url,
                "contents": detail.contents,
                "date": detail.date.isoformat(),
                "date_event_start": detail.date_event_start.isoformat()
                if detail.date_event_start
                else None,
                "date_event_end": detail.date_event_end.isoformat() if detail.date_event_end else None,
            }
        )
        is_active = self._is_active(detail.date_event_start, detail.date_event_end)
        was_inserted = instance is None

        if instance is None:
            # 목록보다 상세가 먼저 들어오거나, 목록 직후 상세를 바로 채우는 경우를 함께 처리합니다.
            instance = NexonNoticeEvent(
                notice_id=notice_id,
                title=detail.title,
                url=detail.url,
                notice_date=detail.date,
                event_start_date=detail.date_event_start,
                event_end_date=detail.date_event_end,
                contents=detail.contents,
                is_active=is_active,
                raw_payload=payload,
            )
            self._db.add(instance)
        else:
            # 상세 본문과 날짜 정보를 기존 레코드에 덮어씁니다.
            instance.title = detail.title
            instance.url = detail.url
            instance.notice_date = detail.date
            instance.event_start_date = detail.date_event_start
            instance.event_end_date = detail.date_event_end
            instance.contents = detail.contents
            instance.is_active = is_active
            instance.raw_payload = payload

        return instance, was_inserted

    @staticmethod
    def _requires_detail_sync(
        instance: NexonNoticeEvent | None,
        item: NexonNoticeEventDTO,
    ) -> bool:
        if instance is None:
            return True

        if not instance.contents:
            return True

        return (
            instance.title != item.title
            or instance.url != item.url
            or instance.notice_date != item.date
            or instance.event_start_date != item.date_event_start
            or instance.event_end_date != item.date_event_end
        )

    @staticmethod
    def _serialize_notice_payload(payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False)

    def _refresh_active_flags(self, now: datetime | None = None) -> None:
        now = now or datetime.now(self._KST)

        for instance in self._db.query(NexonNoticeEvent).all():
            instance.is_active = self._is_active(
                instance.event_start_date,
                instance.event_end_date,
                now=now,
            )

    @staticmethod
    def _is_active(
        event_start_date: datetime | None,
        event_end_date: datetime | None,
        now: datetime | None = None,
    ) -> bool:
        if event_start_date is None or event_end_date is None:
            return False

        now = now or datetime.now(NexonNoticeSyncService._KST)
        start = NexonNoticeSyncService._to_kst(event_start_date)
        end = NexonNoticeSyncService._to_kst(event_end_date)
        current = NexonNoticeSyncService._to_kst(now)

        return start <= current <= end

    @staticmethod
    def _to_kst(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=NexonNoticeSyncService._KST)
        return value.astimezone(NexonNoticeSyncService._KST)
