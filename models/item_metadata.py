from database import Base
from uuid import UUID, uuid4
from datetime import date
from sqlalchemy import UUID as SQLALCHEMY_UUID, ForeignKey, Date, Float, Integer, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

class ItemMetadata(Base):
    __tablename__ = 'item_metadatas'

    __table_args__ = (
        CheckConstraint('easiness_factor>=1.3', name='check_easiness_min'),
        CheckConstraint('inter_repetition>=1', name='check_repetition_min')
    )

    item_id: Mapped[UUID] = mapped_column(
        SQLALCHEMY_UUID,
        ForeignKey('vocabulary_items.id'),
        primary_key=True
    )
    easiness_factor: Mapped[float] = mapped_column(
        Float,
        default=2.5
    )
    inter_repetition: Mapped[int] = mapped_column(
        Integer,
        default=1
    )
    next_repetition_date: Mapped[date] = mapped_column(
        Date,
        default=date.today
    )