"""Re-export the SQLAlchemy base for model modules."""

from app.db.base import Base

__all__ = ["Base"]
