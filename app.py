from fastapi import FastAPI, Request
from fastapi.responses import  JSONResponse
from src.api.cmnd import documentScanner, validation
from pydantic import BaseModel
import src.utils.error_handle as error_handle
from src.api import cmnd, image

# UPLOAD_FOLDER = './cmnd'


app = FastAPI()
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Frontside(BaseModel):
    name: str
    identityNumber: str
    address: str
    birthday: str
    image: str
    imageWidth: int
    imageHeight: int
    identityWidth: int
    identityHeight: int


class DemoImage(BaseModel):
    name: str
    imageWidth: int
    imageHeight: int
    image: str
    identityWidth: int
    identityHeight: int


class Seen(BaseModel):
    name: str


@app.get('/')
def home():
    return "hello"


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file1' not in request.files:
#             return 'there is no file1 in form!'
#         file1 = request.files['file1']
#         path = os.path.join(app.config['UPLOAD_FOLDER'], "a.jpg")
#         file1.save(path)
#         return path


@app.post("/frontside")
def frontside(item: Frontside):
    # data = request.json
    # convert.convert_base64_to_image(item, "frontside")
    path_name = "frontside/{}_frontside.jpg".format(item.name)
    # processImage.cropIdentity(path_name, item)
    print(path_name)
    result = documentScanner.valid_front_side_identity(
        path_name)
    # base64_string=convert.convert_image_to_base64(path_name)
    # result["base64String"] =base64_string
    boool = validation.validate_name(item.name, result["name"])
    print(boool)
    return result






app.include_router(cmnd.router)
app.include_router(image.router)


@app.exception_handler(error_handle.Exception_Handle)
async def MyCustomExceptionHandler(request: Request, exception: error_handle.Exception_Handle):
    return JSONResponse(
        status_code=exception.code,
         content={
             "result": exception.result,
             "field": exception.field,
             "message": exception.message
             })
