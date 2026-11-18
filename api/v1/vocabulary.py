from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.vocabulary import VocabularyCreate, VocabularyCreateResponse, VocabularyResponse, VocabularyPartiallyUpdate
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, delete
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

@router.get('', response_model=list[VocabularyResponse])
async def get_vocabularies(database: Annotated[AsyncSession, Depends(get_session_async)]):
    item_count_query = (
        select(
            VocabularyItem.vocabulary_id,
            func.count(VocabularyItem.id).label('total_items')
        )
        .group_by(VocabularyItem.vocabulary_id)
        .subquery()
    )

    repetition_count_query = (
        select(
            VocabularyItem.vocabulary_id,
            func.count(VocabularyItem.id).label('due_count')
        )
        .outerjoin(VocabularyItem.item_metadata)
        .where(ItemMetadata.next_repetition_date <= date.today())
        .group_by(VocabularyItem.vocabulary_id)
        .subquery()
    )

    result = await database.execute(
        select(
            Vocabulary.id,
            Vocabulary.name,
            func.coalesce(item_count_query.c.total_items, 0).label('total_items'),
            func.coalesce(repetition_count_query.c.due_count, 0).label('due_count')
        )
        .outerjoin(
            item_count_query,
            Vocabulary.id == item_count_query.c.vocabulary_id
        )
        .outerjoin(
            repetition_count_query,
            Vocabulary.id == repetition_count_query.c.vocabulary_id
        )
    )

    return result.mappings().all()

@router.patch('/{vocabulary_id}')
async def partially_update_vocabulary(
    vocabulary_id: UUID,
    data_to_update: VocabularyPartiallyUpdate,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    existing_vocabulary = await database.scalar(
        select(
            select(1)
            .where(Vocabulary.id == vocabulary_id)
            .exists()
        )
    )

    if not existing_vocabulary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Vocabulary with id {vocabulary_id} doesn\'t exists'
        )

    updated_vocabulary = await database.scalar(
        update(Vocabulary)
        .where(Vocabulary.id == vocabulary_id)
        .values(**data_to_update.model_dump(exclude_unset=True))
        .returning(Vocabulary)
    )

    await database.commit()
    return updated_vocabulary

@router.delete('/{vocabulary_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_vocabulary(
    vocabulary_id: UUID,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    existing_vocabulary = await database.scalar(
        select(
            select(1)
            .where(Vocabulary.id == vocabulary_id)
            .exists()
        )
    )

    if not existing_vocabulary:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Vocabulary with id {vocabulary_id} doesn\'t exists'
        )

    await database.execute(
        delete(Vocabulary)
        .where(Vocabulary.id == vocabulary_id)
    )
    await database.commit()