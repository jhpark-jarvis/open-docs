"""Service for syncing Nexon notices into the database."""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime, timezone
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
        # 목록 API를 호출한 뒤, DB에 upsert 가능한 형태로 넘깁니다.
        notice_events = await self._client.fetch_notice_events()
        return self._upsert_notice_events(notice_events)

    def _upsert_notice_events(
        self, notice_events: Sequence[NexonNoticeEventDTO]
    ) -> tuple[list[NexonNoticeEvent], int, int]:
        # 목록 응답 기준으로 신규/갱신 건수를 집계합니다.
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

            # 원본 응답을 디버깅/추적용 payload로 보관합니다.
            payload = json.dumps(
                {
                    "title": item.title,
                    "url": item.url,
                    "notice_id": item.notice_id,
                    "date": item.date.isoformat(),
                    "date_event_start": item.date_event_start.isoformat()
                    if item.date_event_start
                    else None,
                    "date_event_end": item.date_event_end.isoformat() if item.date_event_end else None,
                },
                ensure_ascii=False,
            )
            is_active = self._is_active(item.date_event_start, item.date_event_end)

            if instance is None:
                # 최초 수집된 공지는 새 레코드로 저장합니다.
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
                inserted += 1
            else:
                # 이미 있던 공지는 최신 정보로 갱신합니다.
                instance.title = item.title
                instance.url = item.url
                instance.notice_date = item.date
                instance.event_start_date = item.date_event_start
                instance.event_end_date = item.date_event_end
                instance.is_active = is_active
                instance.raw_payload = payload
                updated += 1

            # 저장 후 반환용 리스트에 모읍니다. is_active 같은 후속 컬럼도 여기서 함께 갱신될 수 있습니다.
            saved.append(instance)

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

        # 상세 응답도 그대로 보관해두면 나중에 스키마를 바꾸기 쉽습니다.
        payload = json.dumps(
            {
                "title": detail.title,
                "url": detail.url,
                "contents": detail.contents,
                "date": detail.date.isoformat(),
                "date_event_start": detail.date_event_start.isoformat()
                if detail.date_event_start
                else None,
                "date_event_end": detail.date_event_end.isoformat() if detail.date_event_end else None,
            },
            ensure_ascii=False,
        )
        is_active = self._is_active(detail.date_event_start, detail.date_event_end)

        if instance is None:
            # 목록보다 상세가 먼저 들어오는 경우를 대비해 예외 없이 생성합니다.
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

        # 상세 동기화도 하나의 저장 단위로 commit합니다.
        self._db.commit()
        self._db.refresh(instance)
        return instance

    @staticmethod
    def _is_active(
        event_start_date: datetime | None,
        event_end_date: datetime | None,
        now: datetime | None = None,
    ) -> bool:
        if event_start_date is None or event_end_date is None:
            return False

        now = now or datetime.now(NexonNoticeSyncService._KST)
        start = NexonNoticeSyncService._to_kst(event_start_date).date()
        end = NexonNoticeSyncService._to_kst(event_end_date).date()
        today = NexonNoticeSyncService._to_kst(now).date()

        return start <= today <= end

    @staticmethod
    def _to_kst(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=NexonNoticeSyncService._KST)
        return value.astimezone(NexonNoticeSyncService._KST)
