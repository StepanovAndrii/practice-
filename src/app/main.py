from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from src.app.routers.view import vocabulary
from src.app.routers.api import vocabulary_item
from src.app.routers.api import authentication, sentence, suggestion
from src.app.routers.view import home

from src.app.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)
app.include_router(home.router)
app.include_router(vocabulary.router)

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(authentication.router)
api_router.include_router(vocabulary_item.router)
api_router.include_router(sentence.router)
api_router.include_router(suggestion.router)

app.include_router(api_router)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get('/health', tags=['health'])
async def check_health():
    return {'status': 'Running'}