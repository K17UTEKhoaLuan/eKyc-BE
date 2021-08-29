# import cv2
# import numpy as np
# import utils

# webCamFeed = True
# pathImage = "1.jpg"
# cap = cv2.VideoCapture(1)
# cap.set(10, 160)
# heightImg = 640
# widthImg = 480


# utils.initializeTrackbars()
# count = 0

# while True:
#     # Blank image
#     imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
#     if webCamFeed:
#         success, img = cap.read()
#     else:
#         img = cv2.imread(pathImage)
#     img = cv2.resize(img, (widthImg, heightImg))
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
#     thres = utils.valTrackbars()
#     imgThreshold = cv2.Canny(imgBlur,thres[0], thres[1])
#     kernel = np.ones((5,5))
#     imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
#     imgThreshold = cv2.erode(imgDial, kernel, interations =1)


from shlex import split
import cv2
import numpy as np
import string
# import easyocr
# from PIL import Image
import pytesseract as pt
import re
import dlib
import compare_image
# tessdata_dir_config = r'--tessdata-dir "/app/.apt/usr/share/tesseract-ocr/4.00/tessdata"'
tessdata_dir_config = r'--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'
# pt.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
###################################
widthImg = 856
heightImg = 539
#####################################

# cap = cv2.VideoCapture(1)
# cap.set(10, 150)


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", imgGray)
    # imgBlur = cv2.GaussianBlur(imgGray, (1,1), 1)
    # cv2.imshow("blur",imgBlur)
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


def cropImageIdentifyNumber(img):
    y = 115
    x = 405
    h = 190
    w = 700
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyNameLineOne(img):
    y = 165
    x = 360
    h = 249
    w = 840
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyNameLineTwo(img):
    y = 227
    x = 228
    h = 290
    w = 850
    crop = img[y:h, x:w]
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return crop


def cropImageIdentifyBirthday(img):
    y = 285
    x = 400
    h = 350
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
            # print("x:",x)
            # print("y:",y)
            # Draw a circle
            cv2.circle(img=img, center=(x, y), radius=2,
                       color=(0, 0, 255), thickness=1)
    # show the imageimg
    # cv2.imshow(winname="Face", mat=img)


def split_string(pre_string):
    chars = re.escape(string.punctuation)
    return re.split(r'['+chars+" |\n"+']', pre_string)


def scan_name(img):
    imgCropNameLineOne = cropImageIdentifyNameLineOne(img)
    imgCropNameLineTwo = cropImageIdentifyNameLineTwo(img)
    # cv2.imshow("name", imgCropNameLineOne)
    # cv2.imshow("name1", imgCropNameLineTwo)
    # name = reader.readtext(imgCropNameLineOne) if(len(reader.readtext(
    #     imgCropNameLineOne)) > 0) else reader.readtext(imgCropNameLineTwo)
    nameOne = pt.image_to_string(
        imgCropNameLineOne, lang='eng', config=tessdata_dir_config)
    nameTwo = pt.image_to_string(
        imgCropNameLineTwo, lang='eng', config=tessdata_dir_config)
    return nameOne + nameTwo
    if(len(name) > 0):
        chars = re.escape(string.punctuation)
        return re.sub(r'['+chars+']', ' ', (name[0])[1])
    else:
        return ""


def scan_identify_number(img):
    imgCropNumber = cropImageIdentifyNumber(img)
    # number = reader.readtext(imgCropNumber)
    number = pt.image_to_string(
        imgCropNumber, lang='eng', 
        config=tessdata_dir_config+' --psm 9 --oem 1 -c tessedit_char_whitelist=0123456789 ')
    number = split_string(number)
    # return a
    if(len(number) > 0):
        for num in number:
            if (len(num) == 9):
                return num
        return ""
    else:
        return ""


def scan_birthday(img):
    imgCropBirthday = cropImageIdentifyBirthday(img)
    # birthday = reader.readtext(imgCropBirthday)
    # cv2.imshow("a",imgCropBirthday)
    # birthday = pt.image_to_string(
    #     imgCropBirthday, config=tessdata_dir_config)
    # thr = cv2.threshold(src=imgCropBirthday, thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow("th", thr)
    birthday = pt.image_to_string(imgCropBirthday, lang='eng',
                                  config=tessdata_dir_config+' --psm 9 --oem 1 -c tessedit_char_whitelist=0123456789-O0 ')
    chars = """!"\#\$%\&'\(\)\*\+,./:;<=>\?@\[\\\]\^_`\{\|\}\~"""
    print(chars)
    birthday = re.split(r'[|\n |\f |\x0c]', birthday)
    print(birthday)
    # birthday = birthday.split(" ")
    # print(birthday)
    # return birthday
    if(len(birthday) > 0):
        for sub_birth in birthday:
            print(sub_birth)
            day_month_year = sub_birth.split("-")
            if(len(day_month_year) == 3):
                return sub_birth
        return ""
    else:
        return ""


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
        # imageArray = ([img,imgThres],
        #           [imgContour,imgWarped])
        imageArray = ([imgContour, imgWarped])
        # cv2.imshow("ImageWarped", imgWarped)
        imgCropImage = cropImageIdentifyImage(imgWarped)
        # imgCrop = cv2.Canny(imgCrop, 10, 400)
        # cv2.imshow("ImageCroped", imgCropNameLineTwo)
        # cv2.imshow("ImageCropedOne", imgCropNameLineOne)
        # cv2.imshow("ImageCropedNumber", imgCropNumber)
        # cv2.imshow("ImageCropedBirthday", imgCropBirthday)
        # cv2.imshow("ImageCropedImage", cv2.cvtColor(
        #     imgCropImage, cv2.COLOR_BGR2RGB))
        # cv2.imwrite("a.jpg", imgCropImage)
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
        #imgCropNameLineOne = cropImageIdentifyNameLineOne(imgWarped)

        chars = re.escape(string.punctuation)
        # print(chars)
        # img_text=re.sub(r'['+chars+']', '',img_text)
        # numberr = (number[0])[1]
        name = re.sub(r'['+chars+"‘"+']', '', name)
        # print(img_text)
        print("+"+name+"+")
        print("number", number)
        print("birthday", birthday)
        print(distance, result)
        return {
            "result": True,
            "number": number,
            "birthday": birthday
        }
    else:
        # imageArray = ([img, imgThres],
        #               [img, img])
        # imageArray = ([imgContour, img])
        return {
            "result": False
        }

    # stackedImages = stackImages(0.6, imageArray)
    # cv2.imshow("WorkFlow", stackedImages)

    # if cv2.waitKey(1) and 0xFF == ord('q'):
    #     break

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
