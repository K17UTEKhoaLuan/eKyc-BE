from fastapi import APIRouter, responses
from .controller import router as cmnd_router
router = APIRouter()
router.include_router(
    cmnd_router,
    prefix="/cccd",
    tags=["cccd"],
    responses={
        404: {
            "description": "Not Found"
        }
    })
