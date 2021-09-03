from fastapi import APIRouter, responses
from .router import router as cmnd_router
router = APIRouter()
router.include_router(
    cmnd_router,
    prefix="/cmnd",
    tags=["cmnd"],
    responses={
        404: {
            "description": "Not Found"
        }
    })
