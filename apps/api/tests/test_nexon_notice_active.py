from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

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
