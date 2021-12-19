from fastapi import APIRouter, File, UploadFile, Request
from . import documentScanner
from ...api.image import convert
from .model import Identity
from .validation import (validate_name,
                         validate_birthday,
                         validate_number_identity,
                         validate_province_identity_number,
                         validate_province_identity_number2,
                         validate_release_date,
                         validate_name2)
from src.process import processImage
import cv2
from src.utils.success_handle import success_return
from .middleware import check_value_scaned_is_none
router = APIRouter()


@router.post("/validation")
def validation(item: Identity, request: Request):
    print(item.address)
    img_frontside = convert.convert_base64_to_image(item.frontside)
    img_frontside = documentScanner.resize_and_pre(img_frontside)
    img_backside = convert.convert_base64_to_image(item.backside)
    img_backside = documentScanner.resize_and_pre(img_backside)
    success, scaned_name = documentScanner.scan_name(img_frontside)
    print(success)
    check_value_scaned_is_none(success)
    success, scaned_identity_number = documentScanner.scan_identify_number(
        img_frontside)
    check_value_scaned_is_none(success)
    success, scaned_birthday = documentScanner.scan_birthday(img_frontside)
    check_value_scaned_is_none(success)
    success, scaned_province = documentScanner.scan_province(img_backside)
    check_value_scaned_is_none(success)
    success, scaned_release_date = documentScanner.scan_release_date(
        img_backside)
    check_value_scaned_is_none(success)
    print("scaned_release_date", scaned_release_date)
    print("scaned_province", scaned_province)
    print("scaned_name", scaned_name)
    print("scaned_identity_number", scaned_identity_number)
    print("scaned_birthday", scaned_birthday)
    validate_name2(item.name, scaned_name)
    validate_number_identity(item.identityNumber, scaned_identity_number)
    validate_birthday(item.birthday, scaned_birthday)
    validate_province_identity_number2(
        scaned_identity_number, scaned_province)
    validate_release_date(scaned_release_date)
    face_img = processImage.cropImageIdentifyImage(img_frontside)
    cv2.imwrite(
        "savedata/face_from_identity/{}.jpg".format(item.identityNumber), face_img)
    return success_return(result=True,
                          message="valid complete",
                          client=request.client.host+":"+str(request.client.port))
    # return {
    #     "result": True,
    #     "message": "valid complete"
    # }
