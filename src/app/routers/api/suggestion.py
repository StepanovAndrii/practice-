from fastapi import APIRouter

router = APIRouter(
    prefix='/practice/sentences/{sentence_id}/suggestion',
    tags=['suggestion']
)

@router.post('/')
async def create_suggestion(sentence_id: int):
    return {'': ''}

@router.get('/')
async def get_suggestion(sentence_id: int):
    return {'': ''}

@router.patch('/')
async def partial_update_suggestion(sentence_id: int):
    return {'': ''}