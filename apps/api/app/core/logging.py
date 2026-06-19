"""Application logging helpers.

Keep this module as the single place for future logging configuration,
structured event metadata, and ECS-friendly formatter setup.
"""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger for the application."""

    return logging.getLogger(name)
