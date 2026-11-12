from fastapi import APIRouter

router = APIRouter()

@router.get('')
async def get_practice_sentences():
    return {'practice': 'sentences'}