from fastapi import FastAPI
from app.routers import receipts
from app.core.config import settings

# Instantiate FastAPI with project metadata for automatic docs
def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )
    # Mount the receipts router at the "/receipts" path
    app.include_router(
        receipts.router,
        prefix="/receipts",
        tags=["receipts"]
    )
    return app

app = create_app() 