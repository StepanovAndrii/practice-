import uvicorn

from fastapi import FastAPI, APIRouter
from api.v1 import vocabulary, vocabulary_item, sentence, suggestion

app = FastAPI()

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(vocabulary_item.router, prefix='/vocabulary/{vocabulary_id}/items', tags=['vocabulary item'])
api_router.include_router(vocabulary.router, prefix='/vocabulary', tags=['vocabulary'])
api_router.include_router(sentence.router, prefix='/sentence', tags=['sentence'])
api_router.include_router(suggestion.router, prefix='/suggestion', tags=['suggestion'])

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app) 