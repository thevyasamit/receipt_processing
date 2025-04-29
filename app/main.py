from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from app.routers import receipts
from app.core.config import settings


# Instantiate FastAPI with project metadata for automatic docs
def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )

    # Custom exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify input."
        )

    # Mount the receipts router at the "/receipts" path
    app.include_router(
        receipts.router,
        prefix="/receipts",
        tags=["receipts"]
    )
    @app.get("/")
    async def root():
        return {"message": "Welcome to the Receipt Processor API. The service is running!"}
    return app


app = create_app() 