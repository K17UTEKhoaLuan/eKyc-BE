from sys import path
from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from numpy.core.numeric import identity
import convert
import documentScanner
import processImage
from pydantic import BaseModel
import os
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
    convert.convert_base64_to_image(item, "frontside")
    path_name = "frontside/{}_frontside.jpg".format(item.name)
    processImage.cropIdentity(path_name, item)
    print(path_name)
    result = documentScanner.valid_front_side_identity(
        path_name)
    base64_string=convert.convert_image_to_base64(path_name)
    result["base64String"] =base64_string
    return result


@app.post("/democrop")
def crop(item: DemoImage):
    convert.convert_base64_to_image(item, "demo")
    processImage.cropIdentity("demo/{}_demo.jpg".format(item.name), item)
    return "done"


@app.get("/seen")
def seen(name: str):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(dir_path, "demo/{}_demo.jpg".format(name))
    # if(os.path.exists(dir_path)):
    #     # return FileResponse(file_path, media_type="image/jpg")
    # else:
    #     return "not exist"
    # _, img = processImage.open_image("demo/{}_demo.jpg".format(name))
    # if(_):
    base64_string=convert.convert_image_to_base64("demo/{}_demo.jpg".format(name))
    return {
        "result": True,
        "base64String":base64_string
    }
    # else:
        # return {
            # "result": False
        # }