"""ORM models for OpenDocs."""

from app.db.base import Base
from app.models.nexon_notice import NexonNoticeEvent

__all__ = ["Base", "NexonNoticeEvent"]
