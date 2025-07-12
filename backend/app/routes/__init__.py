from fastapi import APIRouter
from app.routes.health import router as health
from app.routes.CodePayLoad import router as codePayLoad

# Initialize the main router and include sub-routers
# This file initializes the main router and includes the health and CodePayLoad routers.
router = APIRouter()
router.include_router(health)
router.include_router(codePayLoad)
