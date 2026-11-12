from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLALCHEMY_UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.vocabulary_item import VocabularyItem

class Vocabulary(Base):
    __tablename__ = 'vocabularies'

    id: Mapped[UUID] = mapped_column(
        SQLALCHEMY_UUID,
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    items: Mapped[list[VocabularyItem]] = relationship(
        cascade='all, delete-orphan'
    )