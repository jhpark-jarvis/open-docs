"""Shared Pydantic schema helpers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    """Base schema that supports ORM mode."""

    model_config = ConfigDict(from_attributes=True)
