from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4

class VocabularyBase(BaseModel):
    name: str

class VocabularyInputBase(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True
    )

class VocabularyCreate(VocabularyBase, VocabularyInputBase):
    pass

class VocabularyPartiallyUpdate(VocabularyInputBase):
    name: str

class VocabularyBaseResponse(VocabularyBase):
    id: UUID

class VocabularyCreateResponse(VocabularyBaseResponse):
    pass

class VocabularyResponse(VocabularyBaseResponse):
    total_items: int
    due_count: int