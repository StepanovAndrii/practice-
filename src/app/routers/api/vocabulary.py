from fastapi import APIRouter, Depends
from app.core.models.vocabulary import VocabularyCreate, Vocabulary
from app.core.deps import get_session, AsyncSession

router = APIRouter(prefix='/vocabulary')

@router.post('/')
async def create_vocabulary(
    vocabulary_dto: VocabularyCreate,
    session: AsyncSession = Depends(get_session)
):
    vocabulary_database_model = Vocabulary.model_validate(vocabulary_dto)
    session.add(vocabulary_database_model)
    await session.commit()
    await session.refresh(vocabulary_database_model)
    return vocabulary_database_model