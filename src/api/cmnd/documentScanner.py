#
from shlex import split
import cv2
import numpy as np
import string
import easyocr
# from PIL import Image
import pytesseract as pt
import re
import dlib
from src.api.face import compare_image
from src.process import processImage

###################################
widthImg = 856
heightImg = 539
#####################################
reader = easyocr.Reader(['en'])

# cap = cv2.VideoCapture(1)
# cap.set(10, 150)


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    imgCanny = cv2.Canny(imgGray, 50, 200)
    # cv2.imshow("canny",imgCanny)
    kernel = np.ones((3, 3))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    # cv2.imshow("dial",imgDial)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    # cv2.imshow("thres",imgThres)
    return imgThres


def getContours(img, imgContour):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.06*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest, imgContour


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew


def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32(
        [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))

    return imgCropped


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def detectFace(img):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use detector to find landmarks
    faces = detector(gray)

    for face in faces:
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Draw a rectangle
        cv2.rectangle(img=img, pt1=(x1, y1), pt2=(
            x2, y2), color=(0, 255, 0), thickness=4)

        face_features = predictor(image=gray, box=face)

        # Loop through all 68 points
        for n in range(0, 68):
            x = face_features.part(n).x
            y = face_features.part(n).y
          
            cv2.circle(img=img, center=(x, y), radius=2,
                       color=(0, 0, 255), thickness=1)



def split_string(pre_string):
    chars = re.escape(string.punctuation)

    pre_string = " ".join(pre_string.split())
    # print("pre_string",pre_string)
    list_string = re.split(r'['+chars+" |?? |\n |\f |\x0c"+']', pre_string)
    while '' in list_string:
        list_string.remove('')
    print(list_string)
    # list_string.remove("")
    return list_string, " ".join(list_string).strip()


def scan_name(img):
    imgCropNameLineOne = processImage.cropImageIdentifyNameLineOne(img)
    imgCropNameLineTwo = processImage.cropImageIdentifyNameLineTwo(img)

    name1 = reader.readtext(imgCropNameLineOne) 
    name2 = reader.readtext(imgCropNameLineTwo)
    name = ""
    for string_name in name1:
        name += string_name[1]+" "
    for string_name in name2:
        name += string_name[1]+" "

    success = True if len(name) else False
    res_name = name if len(name) else None
    print("res_name", res_name)
    return success, res_name
    return nameOne + nameTwo
    if(len(name) > 0):
        chars = re.escape(string.punctuation)
        return re.sub(r'['+chars+']', ' ', (name[0])[1])
    else:
        return ""


def scan_identify_number(img):
    imgCropNumber = processImage.cropImageIdentifyNumber(img)
    number = reader.readtext(imgCropNumber,allowlist = '0123456789')

    print("identify_number",(number[0])[1] if number else "")


    res_number = None
    success = False
    if(len(number) > 0):
        for num in number:
            if (len(num[1]) == 9):
                res_number = num[1]
                success = True
    return success, res_number


def scan_birthday(img):
    imgCropBirthday = processImage.cropImageIdentifyBirthday(img)
    birthday = reader.readtext(imgCropBirthday,allowlist = '0123456789-')

    print("birthday", birthday)

    res_birthday = None
    success = False
    if(len(birthday) > 0):
        for sub_birth in birthday:
            print(sub_birth[1])
            day_month_year = sub_birth[1].split("-")
            if(len(day_month_year) == 3):
                res_birthday= sub_birth[1]
                success = True
    return success, res_birthday


def scan_province(img):
    img_croped = processImage.crop_image_province(img)

    province = reader.readtext(img_croped)
    print(province)
    success = True if(province)else False
    res_province = province if(province) else None
    return success,res_province


def scan_release_date(img):
    img_croped = processImage.crop_image_release_date(img)

    number = reader.readtext(img_croped,allowlist = '0123456789')
    print(number)
    success = True if(number and len(number[0][1]) == 4) else False
    res_number = number[0][1]  if(number and len(number[0][1]) == 4) else None
    return success, res_number


def resize_and_pre(img):
    img = cv2.resize(img, (widthImg, heightImg))
    return img


def valid_front_side_identity(img_name):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)
    # cv2.imshow("a", imgThres)
    biggest, imgContour = getContours(imgThres, imgContour)
    print(biggest)
    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)

        imageArray = ([imgContour, imgWarped])
        # cv2.imshow("ImageWarped", imgWarped)
        print(type(imgWarped))
        imgCropImage = processImage.cropImageIdentifyImage(imgWarped)

        distance, result = compare_image.main(cv2.cvtColor(
            imgCropImage, cv2.COLOR_BGR2RGB), cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        detectFace(imgCropImage)
        # img_object = cv2.Canny(img_object,0,10)
        #######################################################
        # reader = easyocr.Reader(['en'])
        number = scan_identify_number(imgWarped)
        birthday = scan_birthday(imgWarped)
        name = scan_name(imgWarped)
        #######################################################
        # imgCropNameLineOne = cropImageIdentifyNameLineOne(imgWarped)

        chars = re.escape(string.punctuation)

        name = re.sub(r'['+chars+"???"+']', '', name)
        # print(img_text)
        print("name", name)
        print("number", number)
        print("birthday", birthday)
        print(distance, result)

        return {
            "result": True,
            "number": number,
            "birthday": birthday,
            "name": name
        }
    else:

        return {
            "result": False
        }

