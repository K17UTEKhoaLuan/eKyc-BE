from fastapi import APIRouter, File, UploadFile, Request
from src.process import processImage
from ...api.image import convert
from .validation import (validate_release_date,
                          validate_sex,
                          validate_province_identity_number,
                          validate_birthday,
                          validate_identity_number
                        )
from src.utils.success_handle import success_return
from .model import Identity
import cv2

router = APIRouter()

@router.post("/validation")
def validation(item: Identity,request: Request):
  img_frontside = convert.convert_base64_to_image(item.frontside)
  img_frontside = processImage.resize_and_pre(img_frontside)
  validate_identity_number(item.identityNumber)
  validate_release_date(item.birthday)
  validate_sex(item)
  validate_province_identity_number(item)
  validate_birthday(item)
  face_img = processImage.cropImageCCCDImage(img_frontside)
  cv2.imwrite(
        "savedata/face_from_identity/{}.jpg".format(item.identityNumber), face_img)
  return success_return(result=True,
                          message="valid complete",
                          client=request.client.host+":"+str(request.client.port))