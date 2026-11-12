from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.vocabulary import VocabularyCreate, VocabularyCreateResponse, VocabularyResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.inspection import inspect
from database import get_session_async
from models.vocabulary import Vocabulary
from models.vocabulary_item import VocabularyItem
from models.item_metadata import ItemMetadata
from datetime import date

router = APIRouter()

@router.post('',
             response_model=VocabularyCreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create_vocabulary(
    vocabulary: VocabularyCreate,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    result = await database.execute(
        select(
            Vocabulary
        ).where(
            Vocabulary.name == vocabulary.name
        ) #todo: if same user have same vocabulary title
    ) 

    existing_vocabulary = result.scalars().first()

    if existing_vocabulary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vocabulary name already exists'
        )

    new_vocabulary = Vocabulary(
        name=vocabulary.name
    )

    database.add(new_vocabulary)
    await database.commit()
    await database.refresh(new_vocabulary)

    return new_vocabulary

@router.get('',
            response_model=list[VocabularyResponse])
async def get_vocabularies(database: Annotated[AsyncSession, Depends(get_session_async)]):
    total_items_query = select(
        func.count(VocabularyItem.id)
    ).where(
        Vocabulary.id == VocabularyItem.vocabulary_id
    ).scalar_subquery().label(
        'total_items'
    )

    due_count_query = select(
        func.count(VocabularyItem.id)
    ).where(
        VocabularyItem.item_metadata.has(
            ItemMetadata.next_repetition_date <= date.today()
        ),
        VocabularyItem.vocabulary_id == Vocabulary.id
    ).scalar_subquery().label(
        'due_count'
    )

    result = await database.execute(
        select(
            Vocabulary,
            total_items_query,
            due_count_query
        )
    )

    return [
        VocabularyResponse.model_validate({
            **inspect(row.Vocabulary).dict,
            'total_items': row.total_items,
            'due_count': row.due_count
        }) for row in result.mappings()
    ]
    

# @router.delete('/{vocabulary_id}')
# async def delete_vocabulary(vocabulary_id: UUID):
    