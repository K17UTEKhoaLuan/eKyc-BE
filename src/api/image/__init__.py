from fastapi import APIRouter
from .controller import router as image_router
router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={
        404: {
            "description": "Not Found"
        }
    }
)

router.include_router(image_router)


