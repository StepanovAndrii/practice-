from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class VocabularyItemBase(BaseModel):
    term: str
    translation: str | None

class VocabularyItemCreate(VocabularyItemBase):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True
    )

class VocabularyItemResponse(VocabularyItemBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    created_at: datetime