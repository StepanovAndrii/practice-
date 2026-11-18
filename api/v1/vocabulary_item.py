from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from database import get_session_async
from schemas.vocabulary_item import VocabularyItemCreate
from models.vocabulary_item import VocabularyItem
from models.vocabulary import Vocabulary
from models.item_metadata import ItemMetadata

router = APIRouter()

@router.post('',
             status_code=status.HTTP_201_CREATED)
async def create_vocabulary_items(
    vocabulary_id: UUID,
    vocabulary_item: VocabularyItemCreate,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    vocabulary_exists = (await database.scalars(
        select(
            select(1)
            .where(
                Vocabulary.id == vocabulary_id
            ).exists()
        )
    )).first()

    if not vocabulary_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    vocabulary_item_exists = (await database.scalars(
        select(
            select(1)
            .where(
                VocabularyItem.term == vocabulary_item.term,
                VocabularyItem.vocabulary_id == vocabulary_id
            ).exists()
        )
    )).first()

    if vocabulary_item_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='The same vocabulary item already exists'
        )

    new_vocabulary_item = VocabularyItem(
        vocabulary_id = vocabulary_id,
        item_metadata = ItemMetadata(),
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
    vocabulary_exists = (await database.scalars(
        select(
            select(1)
            .where(
                Vocabulary.id == vocabulary_id
            ).exists()
        )
    )).first()

    if not vocabulary_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Vocabulary with id {vocabulary_id} is not found')
    
    return (await database.scalars(
        select(VocabularyItem)
        .where(VocabularyItem.vocabulary_id == vocabulary_id)
    )).all()

@router.delete(
        '/{item_id}',
        status_code=status.HTTP_204_NO_CONTENT)
async def delete_vocabulary_item(
    vocabulary_id: UUID,
    item_id: int,
    database: Annotated[AsyncSession, Depends(get_session_async)]
):
    vocabulary_exists = await database.scalar(
        select(
            select(1)
            .where(Vocabulary.id == vocabulary_id)
            .exists()
        )
    )

    if not vocabulary_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Vocabulary with id {vocabulary_id} doesn\'t exist')

    item_exists = await database.scalar(
        select(
            select(1)
            .where(VocabularyItem.id == item_id,
                   VocabularyItem.vocabulary_id == vocabulary_id)
            .exists()
        )
    )

    if not item_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Vocabulary item with id {item_id} doesn\'t exist'
        )

    await database.execute(
        delete(VocabularyItem)
        .where(VocabularyItem.id == item_id)
    )

    await database.commit()