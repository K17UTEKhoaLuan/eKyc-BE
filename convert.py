import base64
import cv2
# file = 'mat.png'
# image = open(file, 'rb')
# image_read = image.read()
# image_64_encode = base64.encodebytes(image_read) #encodestring also works aswell as decodestring

# print('This is the image in base64: ' + str(image_64_encode))


def convert_base64_to_image(data, dir):        
    image_64_decode = base64.b64decode(str(data["image"])) 
    image_result = open('{}/{}_{}.jpg'.format(dir, data["name"], dir), 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)

