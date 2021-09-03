from fastapi import APIRouter

router = APIRouter()

@router.get("/asd")
def asd(): return True