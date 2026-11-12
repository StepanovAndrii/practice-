from sqlalchemy import UUID as SQLALCHEMY_UUID, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from uuid import UUID, uuid4
from datetime import datetime, UTC

from models.item_metadata import ItemMetadata

class VocabularyItem(Base):
    __tablename__ = 'vocabulary_items'

    id: Mapped[UUID] = mapped_column(
        SQLALCHEMY_UUID,
        default=uuid4,
        primary_key=True
    )
    term: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    translation: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
    vocabulary_id: Mapped[UUID] = mapped_column(
        SQLALCHEMY_UUID,
        ForeignKey('vocabularies.id'),
        nullable=False,
        index=True
    )

    item_metadata: Mapped[ItemMetadata] = relationship(
        uselist=False,
        cascade='all, delete-orphan'
    )