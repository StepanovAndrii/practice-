from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from pydantic import EmailStr

class UserBase(SQLModel):

    name: str = Field(
        max_length=50,
        nullable=False
    )
    email: EmailStr = Field(
        max_length=255,
        unique=True,
        nullable=False
    )

class UserCreate(UserBase):
    google_id: str = Field(
        unique=True
    )

class UserRead(UserBase):
    pass

class User(UserBase, table=True):
    __tablename__ = 'users' #  type: ignore
    
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )