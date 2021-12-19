from fastapi import APIRouter, File, UploadFile, Request
from . import location
from src.utils.success_handle import success_return
router = APIRouter()


@router.get("/province")
def getProvice(request: Request):
    province = location.getProvince()
    return success_return(result=True,
                          message="get province success",
                          data=province,
                          client=request.client.host+":"+str(request.client.port))
