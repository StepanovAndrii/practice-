from datetime import date
from uuid import UUID
from sqlmodel import Field, SQLModel

class ItemMetadata(SQLModel, table=True):
    __tablename__ = 'item_metadatas' #type: ignore

    item_id: UUID = Field(
        primary_key=True,
        foreign_key='item.id'
    )
    easiness_factor: float = Field(
        default=2.5,
        ge=1.3
    )
    inter_repetition: int = Field(
        default=1,
        ge=1
    )
    next_repetition_date: date = Field(
        default=date.today
    )