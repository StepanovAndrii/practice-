from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class VocabularyBase(SQLModel):
    name: str

class VocabularyCreate(VocabularyBase):
    model_config = {
        'extra': 'forbid',
        'str_strip_whitespace': True
    }

class VocabularyRead(VocabularyBase):
    model_config = {
        'from_attributes': True
    }

class Vocabulary(VocabularyBase, table=True):
    __tablename__ = 'vocabularies' #type: ignore

    id: UUID = Field(
        default=uuid4
    )