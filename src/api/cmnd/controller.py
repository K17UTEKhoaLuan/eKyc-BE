import re
from typing import List
import shutil
import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile
from . import documentScanner
from ...api.image import convert
from .model import Identity
from .validation import validate_name, validate_birthday, validate_number_identity, validate_province_identity_number
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
    
    print("scaned_province",scaned_province)
    print("scaned_name",scaned_name)
    print("scaned_identity_number",scaned_identity_number)
    print("scaned_birthday",scaned_birthday)
    # validate_name(item.name, scaned_name)
    # validate_number_identity(item.identityNumber, scaned_identity_number)
    # validate_birthday(item.birthday, scaned_birthday)
    validate_province_identity_number(scaned_identity_number,scaned_province)
    return {
        "result": True,
        "message": "valid complete"
    }


@router.post("/uploadvideo")
async def create_upload_file(name: str,file: UploadFile = File(...)):
    # file_name =""
    # file_name+=file.filename
    contents = file.file.read()
    print(type(contents))
    with open("{}.mp4".format(name), 'wb') as image:
        image.write(contents)
        image.close()
    #     # shutil.copyfileobj(file.file,"a.mp4")
        # nparr = np.fromstring(contents, np.uint8)
        # img_np = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
    #     decoded = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)
        # print(img_np)
    #     print('OpenCV:\n', img_np)
    # cap  = cv2.VideoCapture("20210130_175032.mp4")
    # while(cap.isOpened()):
    #     ret, frame = cap.read()
    #     cv2.imshow('frame',frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()
    return {
        "result": True,
        "message": "Upload video success"
    }
