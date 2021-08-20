from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.templating import Jinja2Templates
import os
import convert
import documentScanner
from pydantic import BaseModel
# UPLOAD_FOLDER = './cmnd'


app = FastAPI()
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Frontside(BaseModel):
    name: str
    image: str

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
def frontside(item:Frontside):
    # data = request.json
    convert.convert_base64_to_image(item, "frontside")
    print("frontside/{}_frontside.jpg".format(item.name))
    documentScanner.valid_front_side_identity("frontside/{}_frontside.jpg".format(item.name))
    return "done"


