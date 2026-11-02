from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Item(SQLModel, table=True):
    __tablename__='items' #type: ignore

    id: UUID = Field(
        default=uuid4,
        primary_key=True
    )
    term: str
    translation: str
    created_at: datetime
