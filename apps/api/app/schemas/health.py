"""Schemas for health and readiness endpoints."""

from app.schemas.base import SchemaBase


class HealthResponse(SchemaBase):
    status: str
