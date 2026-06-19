"""Legacy compatibility wrapper for document generation."""

from __future__ import annotations

from app.services.document.document_service import DocumentService

MarkdownDocumentService = DocumentService

__all__ = ["DocumentService", "MarkdownDocumentService"]
