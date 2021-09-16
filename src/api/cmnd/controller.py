from fastapi import APIRouter, File, UploadFile
from . import documentScanner
from ...api.image import convert
from .model import Identity
from .validation import validate_name, validate_birthday, validate_number_identity, validate_province_identity_number, validate_release_date
router = APIRouter()


@router.post("/validation")
def validation(item: Identity):
    img_frontside = convert.convert_base64_to_image(item.frontside)
    img_frontside = documentScanner.resize_and_pre(img_frontside)
    img_backside = convert.convert_base64_to_image(item.backside)
    img_backside = documentScanner.resize_and_pre(img_backside)
    scaned_name = documentScanner.scan_name(img_frontside)
    scaned_identity_number = documentScanner.scan_identify_number(img_frontside)
    scaned_birthday = documentScanner.scan_birthday(img_frontside)
    scaned_province = documentScanner.scan_province(img_backside)
    scaned_release_date = documentScanner.scan_release_date(img_backside)
    print("scaned_release_date",scaned_release_date)
    print("scaned_province",scaned_province)
    print("scaned_name",scaned_name)
    print("scaned_identity_number",scaned_identity_number)
    print("scaned_birthday",scaned_birthday)
    validate_name(item.name, scaned_name)
    validate_number_identity(item.identityNumber, scaned_identity_number)
    validate_birthday(item.birthday, scaned_birthday)
    validate_province_identity_number(scaned_identity_number,scaned_province)
    validate_release_date(scaned_release_date)
    return {
        "result": True,
        "message": "valid complete"
    }

