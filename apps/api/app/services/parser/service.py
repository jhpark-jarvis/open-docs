"""Legacy compatibility wrapper for notice parsing."""

from __future__ import annotations

from app.services.parser.html_parser import NoticeHtmlParser
from app.services.parser.image_extractor import NoticeImageExtractor

NoticeParserService = NoticeHtmlParser

__all__ = ["NoticeImageExtractor", "NoticeParserService"]
