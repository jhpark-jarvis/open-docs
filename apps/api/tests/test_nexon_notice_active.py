from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from app.services.nexon.client import NexonNoticeEvent
from app.services.nexon.sync_service import NexonNoticeSyncService


KST = ZoneInfo("Asia/Seoul")


def test_is_active_returns_true_when_now_is_within_event_window() -> None:
    event_start = datetime(2026, 6, 21, 0, 0, 0, tzinfo=KST)
    event_end = datetime(2026, 6, 21, 23, 59, 59, tzinfo=KST)
    now = datetime(2026, 6, 21, 12, 0, 0, tzinfo=KST)

    assert NexonNoticeSyncService._is_active(event_start, event_end, now=now) is True


def test_is_active_returns_false_when_now_is_outside_event_window() -> None:
    event_start = datetime(2026, 6, 21, 0, 0, 0, tzinfo=KST)
    event_end = datetime(2026, 6, 21, 23, 59, 59, tzinfo=KST)
    now = datetime(2026, 6, 22, 0, 0, 0, tzinfo=KST)

    assert NexonNoticeSyncService._is_active(event_start, event_end, now=now) is False


def test_is_active_returns_false_when_end_time_has_passed_on_same_day() -> None:
    event_start = datetime(2026, 6, 21, 0, 0, 0, tzinfo=KST)
    event_end = datetime(2026, 6, 21, 0, 0, 0, tzinfo=KST)
    now = datetime(2026, 6, 21, 18, 30, 0, tzinfo=KST)

    assert NexonNoticeSyncService._is_active(event_start, event_end, now=now) is False


def test_is_active_returns_true_when_now_matches_end_time() -> None:
    event_start = datetime(2026, 6, 21, 0, 0, 0, tzinfo=KST)
    event_end = datetime(2026, 6, 21, 18, 30, 0, tzinfo=KST)
    now = datetime(2026, 6, 21, 18, 30, 0, tzinfo=KST)

    assert NexonNoticeSyncService._is_active(event_start, event_end, now=now) is True


def test_requires_detail_sync_returns_true_for_new_notice() -> None:
    item = NexonNoticeEvent(
        title="Summer Event",
        url="https://example.com/event",
        notice_id=1001,
        date=datetime(2026, 6, 21, 9, 0, 0, tzinfo=KST),
        date_event_start=datetime(2026, 6, 21, 10, 0, 0, tzinfo=KST),
        date_event_end=datetime(2026, 6, 30, 23, 59, 59, tzinfo=KST),
    )

    assert NexonNoticeSyncService._requires_detail_sync(None, item) is True


def test_requires_detail_sync_returns_true_when_contents_is_missing() -> None:
    item = NexonNoticeEvent(
        title="Summer Event",
        url="https://example.com/event",
        notice_id=1001,
        date=datetime(2026, 6, 21, 9, 0, 0, tzinfo=KST),
        date_event_start=datetime(2026, 6, 21, 10, 0, 0, tzinfo=KST),
        date_event_end=datetime(2026, 6, 30, 23, 59, 59, tzinfo=KST),
    )
    instance = SimpleNamespace(
        title=item.title,
        url=item.url,
        notice_date=item.date,
        event_start_date=item.date_event_start,
        event_end_date=item.date_event_end,
        contents=None,
    )

    assert NexonNoticeSyncService._requires_detail_sync(instance, item) is True


def test_requires_detail_sync_returns_true_when_list_metadata_changes() -> None:
    item = NexonNoticeEvent(
        title="Summer Event Updated",
        url="https://example.com/event",
        notice_id=1001,
        date=datetime(2026, 6, 21, 9, 0, 0, tzinfo=KST),
        date_event_start=datetime(2026, 6, 21, 10, 0, 0, tzinfo=KST),
        date_event_end=datetime(2026, 6, 30, 23, 59, 59, tzinfo=KST),
    )
    instance = SimpleNamespace(
        title="Summer Event",
        url=item.url,
        notice_date=item.date,
        event_start_date=item.date_event_start,
        event_end_date=item.date_event_end,
        contents="cached detail",
    )

    assert NexonNoticeSyncService._requires_detail_sync(instance, item) is True


def test_requires_detail_sync_returns_false_for_unchanged_notice_with_contents() -> None:
    item = NexonNoticeEvent(
        title="Summer Event",
        url="https://example.com/event",
        notice_id=1001,
        date=datetime(2026, 6, 21, 9, 0, 0, tzinfo=KST),
        date_event_start=datetime(2026, 6, 21, 10, 0, 0, tzinfo=KST),
        date_event_end=datetime(2026, 6, 30, 23, 59, 59, tzinfo=KST),
    )
    instance = SimpleNamespace(
        title=item.title,
        url=item.url,
        notice_date=item.date,
        event_start_date=item.date_event_start,
        event_end_date=item.date_event_end,
        contents="cached detail",
    )

    assert NexonNoticeSyncService._requires_detail_sync(instance, item) is False
