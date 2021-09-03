from typing import List
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.get("/validation")
def validateion(): return True

@router.post("/uploadfile")
async def create_upload_file(files: List[UploadFile] = File(...)):
    file_name =""
    for file in files:
        file_name+=file.filename
    return {"filename": file_name}