from fastapi import APIRouter, Request
from src.app.core.templates import templates

router = APIRouter()

@router.get('/vocabulary')
async def get_vocabulary_page(request: Request):
    return templates.TemplateResponse(request, 'vocabulary.html')