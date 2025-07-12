from fastapi import FastAPI
from app.core.config import settings
from app.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

if settings.DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("uvicorn.error")
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode is ON. Logging level set to DEBUG.")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
