import cv2

widthImg = 856
heightImg = 539


def open_image(image_name):
    img = cv2.imread(image_name)
    print(img)
    if(len(img)>0):
        return True, img
    else: 
        return False, ""


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
    coordinate_up_left = (size.imageWidth - size.identityWidth)/2
    coordinate_left_up = (size.imageHeight - size.identityHeight)/2
    y = int(coordinate_up_left)
    h = int(coordinate_up_left + size.identityWidth)
    x = int(coordinate_left_up)
    w = int(coordinate_left_up + size.identityHeight)
    crop = img[y:h, x:w]
    cv2.imwrite("demo/{}_demo.jpg".format(size.name), crop)
    return crop
