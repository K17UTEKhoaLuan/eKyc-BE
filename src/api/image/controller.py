from fastapi import APIRouter, Request
from . import convert
from .model import Image
from .res_model import Crop_Model
from src.process import processImage
from src.utils.success_handle import success_return
router = APIRouter()



@router.post("/crop", response_model=Crop_Model)
def crop_cmnd(data: Image,request: Request):
    # print("string: ", data.image)
    img = convert.convert_base64_to_image(data.image)
    croped_image = processImage.cropIdentity(img=img, item=data)
    base64_string = convert.convert_image_to_base64(croped_image)
    return success_return(
        result=True,
        message= "crop image success",
        client= request.client,
        base64_string = base64_string
    )
    return {
        "result": True,
        "base64_string": base64_string
    }