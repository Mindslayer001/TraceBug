from fastapi import APIRouter
from .views import router as CodePayLoad_Router

router = APIRouter()
router.include_router(CodePayLoad_Router,prefix="/snippets", tags=["Snippets"])