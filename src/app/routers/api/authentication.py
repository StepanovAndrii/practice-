from fastapi import APIRouter

router = APIRouter(
    prefix='/auth/google',
    tags=['authentication']
)

@router.post('/')
async def authenticate_with_google():
    return {'', ''}

@router.post('/callback')
async def catch_google_callback():
    return {'', ''}