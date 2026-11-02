from fastapi import APIRouter

router = APIRouter(
    prefix='/practice/sentences',
    tags=['sentence']
)

@router.get('/')
async def get_practice_sentences():
    return {'practice': 'sentences'}