from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.cmnd import documentScanner, validation
from pydantic import BaseModel
from src.utils.error_handle import Exception_Handle
from src.api import cmnd, image, face, cccd, location
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
    return "hello"



app.include_router(cmnd.router)
app.include_router(image.router)
app.include_router(face.router)
app.include_router(cccd.router)
app.include_router(location.router)


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
