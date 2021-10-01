from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.cmnd import documentScanner, validation
from pydantic import BaseModel
from src.utils.error_handle import Exception_Handle
from src.api import cmnd, image, face
from fastapi.middleware.cors import CORSMiddleware

from src.utils.logging_handle import get_logger
# UPLOAD_FOLDER = './cmnd'

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.1.109:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    # print(__name__)
    # local_logger = get_logger(__name__)
    # local_logger.info(f'I am a local logger.')
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
app.include_router(face.router)


@app.exception_handler(Exception_Handle)
async def MyCustomExceptionHandler(request: Request, exception: Exception_Handle):
    logger = get_logger(exception.name)
    # logger.error(request.client.host+":"+str(request.client.port)+": "+exception.message)
    logger.error("client => {}:{}: {}".format(
        request.client.host, request.client.port, exception.message))
    return JSONResponse(
        status_code=exception.code,
        content={
            "result": exception.result,
            "step": exception.step,
            "field": exception.field,
            "message": exception.message
        })
