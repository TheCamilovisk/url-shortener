"""
Module that defines the URL model for the URL shortener application.

This module provides the URL dataclass mapped to the 'urls' table, representing
the mapping between short codes and original URLs.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Registry for table mappings
table_registry = registry()


@table_registry.mapped_as_dataclass
class URL:
    """
    Data model for a shortened URL.

    Represents the mapping between a short code and its original URL.

    Attributes:
        short_code (str): The unique short code serving as the primary key.
        original_url (str): The full destination URL.
        active (bool): Flag indicating if the URL mapping is active.
        created_at (datetime): Timestamp when the mapping was created.
    """

    __tablename__ = 'urls'

    short_code: Mapped[str] = mapped_column(String(7), primary_key=True)
    original_url: Mapped[str] = mapped_column(String(2048))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=func.now()
    )
