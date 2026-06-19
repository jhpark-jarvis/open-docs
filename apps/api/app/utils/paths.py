"""Filesystem path helpers."""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    """Return the application root directory."""

    return Path(__file__).resolve().parents[3]
