from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class URL:
    __tablename__ = 'urls'

    short_code: Mapped[str] = mapped_column(String(7), primary_key=True)
    original_url: Mapped[str] = mapped_column(String(2048))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=func.now()
    )
