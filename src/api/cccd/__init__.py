from fastapi import APIRouter, responses
from .controller import router as cccd_router
router = APIRouter()
router.include_router(
    cccd_router,
    prefix="/cccd",
    tags=["cccd"],
    responses={
        404: {
            "description": "Not Found"
        }
    })
