import cv2
import PIL.Image
widthImg = 856
heightImg = 539


def open_image(image_name):
    # img = cv2.imread(image_name)
    # if(len(img)>0):
    #     return True, img
    # else: 
    #     return False, ""
    image = open(image_name, 'rb')


def cropImageIdentifyNumber(img):
    y = 115
    x = 405
    h = 190
    w = 700
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropIdentity(img_name, size):
    img = cv2.imread(img_name)
    print(size.name)
    coordinate_up_left = (size.imageHeight - size.identityHeight)/2 
    coordinate_left_up = (size.imageWidth - size.identityWidth)/2
    y = int(coordinate_up_left)
    h = int(coordinate_up_left + size.identityHeight)
    x = int(coordinate_left_up)
    w = int(coordinate_left_up + size.identityWidth)
    crop = img[y:h, x:w]
    cv2.imwrite("frontside/{}_frontside.jpg".format(size.name), crop)
    return crop
