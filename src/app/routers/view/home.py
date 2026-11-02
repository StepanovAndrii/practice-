from fastapi import APIRouter, Request
from src.app.core.templates import templates

router = APIRouter()

@router.get('/', include_in_schema=False)
async def get_home_page(request: Request):
    return templates.TemplateResponse(request, 'home.html')