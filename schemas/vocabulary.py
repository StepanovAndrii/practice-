from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4

class VocabularyBase(BaseModel):
    name: str

class VocabularyCreate(VocabularyBase):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True
    )

class VocabularyBaseResponse(VocabularyBase):
    id: UUID

class VocabularyCreateResponse(VocabularyBaseResponse):
    pass

class VocabularyResponse(VocabularyBaseResponse):
    total_items: int
    due_count: int