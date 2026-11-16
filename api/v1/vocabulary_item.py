from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from database import get_session_async
from schemas.vocabulary_item import VocabularyItemCreate
from models.vocabulary_item import VocabularyItem
from models.vocabulary import Vocabulary

router = APIRouter()

@router.post('',
             status_code=status.HTTP_201_CREATED)
async def create_vocabulary_items(
    vocabulary_id: UUID,
    vocabulary_item: VocabularyItemCreate,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    exists_vocabulary = (await database.scalars(
        select(
            select(1)
            .where(
                Vocabulary.id == vocabulary_id
            ).exists()
        )
    )).first()

    if not exists_vocabulary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    exists_vocabulary_item = (await database.scalars(
        select(
            select(1)
            .where(
                VocabularyItem.term == vocabulary_item.term,
                VocabularyItem.vocabulary_id == vocabulary_id
            ).exists()
        )
    )).first()

    if exists_vocabulary_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='The same vocabulary item already exists'
        )

    new_vocabulary_item = VocabularyItem(
        vocabulary_id = vocabulary_id,
        **vocabulary_item.model_dump()
    )

    database.add(new_vocabulary_item)
    await database.commit()
    await database.refresh(new_vocabulary_item)

    return new_vocabulary_item


@router.get('')
async def get_vocabulary_items(
    vocabulary_id: UUID,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    exists_vocabulary = (await database.scalars(
        select(
            select(1)
            .where(
                Vocabulary.id == vocabulary_id
            ).exists()
        )
    )).first()

    if not exists_vocabulary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return (await database.scalars(
        select(VocabularyItem)
        .where(VocabularyItem.vocabulary_id == vocabulary_id)
    )).all()

@router.delete('/{item_id}')
async def delete_vocabulary_item(vocabulary_id: UUID, item_id: int):
    return {'': ''}