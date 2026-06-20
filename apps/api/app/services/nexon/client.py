"""HTTP client for Nexon OpenAPI communication."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class NexonNoticeEvent:
    title: str
    url: str
    notice_id: int
    date: datetime
    date_event_start: datetime | None
    date_event_end: datetime | None


@dataclass(frozen=True)
class NexonNoticeEventDetail:
    title: str
    url: str
    contents: str
    date: datetime
    date_event_start: datetime | None
    date_event_end: datetime | None


class NexonOpenApiClientError(RuntimeError):
    """Raised when Nexon OpenAPI requests fail."""


class NexonOpenApiClient:
    """Small Nexon OpenAPI client wrapper."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key or settings.nexon_open_api_key
        self._base_url = (base_url or settings.nexon_open_api_base_url).rstrip("/")
        self._timeout = timeout

    async def fetch_notice_events(self) -> list[NexonNoticeEvent]:
        if not self._api_key:
            raise NexonOpenApiClientError("NEXON_OPEN_API_KEY is not configured.")

        url = f"{self._base_url}/maplestory/v1/notice-event"

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(url, headers={"x-nxopen-api-key": self._api_key})

        if response.status_code >= 400:
            raise NexonOpenApiClientError(
                f"Nexon OpenAPI request failed with status {response.status_code}: {response.text}"
            )

        payload: dict[str, Any] = response.json()
        notices = payload.get("event_notice", [])

        return [
            NexonNoticeEvent(
                title=item["title"],
                url=item["url"],
                notice_id=item["notice_id"],
                date=datetime.fromisoformat(item["date"]),
                date_event_start=(
                    datetime.fromisoformat(item["date_event_start"])
                    if item.get("date_event_start")
                    else None
                ),
                date_event_end=(
                    datetime.fromisoformat(item["date_event_end"])
                    if item.get("date_event_end")
                    else None
                ),
            )
            for item in notices
        ]

    async def fetch_notice_event_detail(self, notice_id: int) -> NexonNoticeEventDetail:
        if not self._api_key:
            raise NexonOpenApiClientError("NEXON_OPEN_API_KEY is not configured.")

        url = f"{self._base_url}/maplestory/v1/notice-event/detail"

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                url,
                headers={"x-nxopen-api-key": self._api_key},
                params={"notice_id": notice_id},
            )

        if response.status_code >= 400:
            raise NexonOpenApiClientError(
                f"Nexon OpenAPI detail request failed with status {response.status_code}: {response.text}"
            )

        payload: dict[str, Any] = response.json()
        return NexonNoticeEventDetail(
            title=payload["title"],
            url=payload["url"],
            contents=payload["contents"],
            date=datetime.fromisoformat(payload["date"]),
            date_event_start=(
                datetime.fromisoformat(payload["date_event_start"])
                if payload.get("date_event_start")
                else None
            ),
            date_event_end=(
                datetime.fromisoformat(payload["date_event_end"])
                if payload.get("date_event_end")
                else None
            ),
        )
