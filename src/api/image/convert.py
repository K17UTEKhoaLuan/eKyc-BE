import base64
from os import name
import numpy as np
import cv2
# import src.utils.error_handle as error_handle
from src.utils.error_handle import Exception_Handle


def convert_base64_to_image(img_base64_string):
    if(not img_base64_string.strip()):
        raise Exception_Handle(code=404, message="image is Empty")
    image_64_decode = base64.b64decode(str(img_base64_string))
    im_arr = np.frombuffer(image_64_decode, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    if(img is None):
        raise Exception_Handle(code=400, message="decode error")
    return img
    # image_result = open('{}/{}_{}.jpg'.format(dir, data.name, dir), 'wb') # create a writable image and write the decoding result
    # image_result.write(image_64_decode)


def convert_image_to_base64(img):
    if(img is None):
        raise Exception_Handle(code=400, message="decode error")
    _, image_byte = cv2.imencode(".jpg", img)
    # image = open(file, 'rb')
    # image_read = image.read()
    image_64_encode = base64.b64encode(image_byte)
    if(not image_64_encode.strip()):
        raise Exception_Handle(code=404, message="image is Empty")
    return image_64_encode
