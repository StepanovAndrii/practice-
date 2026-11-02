from fastapi import APIRouter

router = APIRouter(
    prefix='/vocabulary/{vocabulary_id}/items',
    tags=['vocabulary item']
)

@router.post('/')
async def create_vocabulary_items(vocabulary_id: int):
    return {'message': 'Hello!'}

@router.get('/')
async def get_vocabulary_items(vocabulary_id: int):
    return {'message': 'Hello!'}

@router.delete('/{item_id}')
async def delete_vocabulary_item(vocabulary_id: int, item_id: int):
    return {'': ''}