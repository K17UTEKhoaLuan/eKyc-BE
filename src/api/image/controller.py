import base64
from fastapi import APIRouter
from . import convert
from .model import Image
from .res_model import Crop_Model
from src.process import processImage
router = APIRouter()



@router.post("/crop", response_model=Crop_Model)
def crop_cmnd(data: Image):
    img = convert.convert_base64_to_image(data.image)
    croped_image = processImage.cropIdentity(img=img, item=data)
    base64_string = convert.convert_image_to_base64(croped_image)
    return {
        "result": True,
        "base64_string": base64_string
    }