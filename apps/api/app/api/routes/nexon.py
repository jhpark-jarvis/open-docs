from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.nexon_notice import (
    NexonNoticeEventDetailResponse,
    NexonNoticeEventItem,
    NexonNoticeSyncResponse,
)
from app.services.nexon.sync_service import NexonNoticeSyncService

router = APIRouter(prefix="/nexon", tags=["nexon"])


@router.post("/notice-events/sync", response_model=NexonNoticeSyncResponse)
async def sync_notice_events(db: Session = Depends(get_db)) -> NexonNoticeSyncResponse:
    service = NexonNoticeSyncService(db)
    saved, inserted, updated = await service.sync_notice_events()
    return NexonNoticeSyncResponse(
        total=len(saved),
        inserted=inserted,
        updated=updated,
        notices=[
            NexonNoticeEventItem(
                title=item.title,
                url=item.url,
                notice_id=item.notice_id,
                date=item.notice_date,
                date_event_start=item.event_start_date,
                date_event_end=item.event_end_date,
            )
            for item in saved
        ],
    )


@router.get("/notice-events/{notice_id}/detail", response_model=NexonNoticeEventDetailResponse)
async def get_notice_event_detail(
    notice_id: int, db: Session = Depends(get_db)
) -> NexonNoticeEventDetailResponse:
    service = NexonNoticeSyncService(db)
    saved = await service.sync_notice_event_detail(notice_id)
    return NexonNoticeEventDetailResponse(
        title=saved.title,
        url=saved.url,
        contents=saved.contents or "",
        date=saved.notice_date,
        date_event_start=saved.event_start_date,
        date_event_end=saved.event_end_date,
    )
