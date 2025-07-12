
from fastapi import APIRouter
from .schemas import HealthOut

router = APIRouter()
@router.get("/", response_model=HealthOut)
def root():
    return HealthOut(message="TraceBit is running 🚀")