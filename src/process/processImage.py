import re
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


def cropIdentity(img, item):
    coordinate_up_left = (item.imageWidth - item.identityWidth)/2
    coordinate_left_up = (item.imageHeight - item.identityHeight)/2
    print("coordinate_up_left", coordinate_up_left+"-->" +
          int(coordinate_up_left + item.identityWidth))
    print("coordinate_left_up", coordinate_left_up+"-->" +
          int(coordinate_left_up + item.identityHeight))

    y = int(coordinate_up_left)+50
    h = int(coordinate_up_left + item.identityWidth)-50
    x = int(coordinate_left_up)+20
    w = int(coordinate_left_up + item.identityHeight)-20
    crop = img[y:h, x:w]
    # cv2.imwrite("frontside/{}_frontside.jpg".format(size.name), crop)
    return crop


def cropImageIdentifyNumber(img):
    y = 115
    x = 405
    h = 160
    w = 700
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyNameLineOne(img):
    y = 175
    x = 360
    h = 249
    w = 840
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyNameLineTwo(img):
    y = 235
    x = 228
    h = 290
    w = 850
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyBirthday(img):
    y = 260
    x = 400
    h = 320
    w = 840
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyImage(img):
    y = 180
    x = 0
    h = 520
    w = 260
    crop = img[y:h, x:w]
    # crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def crop_image_province(img):
    y = 295
    x = 555
    h = 332
    w = 831
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def crop_image_release_date(img):
    y = 255
    x = 710
    h = 295
    w = 828
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop
