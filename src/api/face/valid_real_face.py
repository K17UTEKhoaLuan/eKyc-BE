import cv2
import mediapipe as mp
# import time
from src.utils.error_handle import Exception_Handle
from src.api.face import compare_image
import json
import os

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
arr = []


def validate_gesture(img, pose_json):
    results = pose.process(img)
    print(pose_json)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(
            img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            if id == 0:
                print("x",lm.x )
                print("y",lm.y)
            if id == 0 and (pose_json["x"])["min"] <= lm.x <= (pose_json["x"])["max"] and (pose_json["y"])["min"] <= lm.y <= (pose_json["y"])["max"]:
                return True
    return False


def get_gesture(identity_number):
    with open("savedata/gesture/{}.json".format(identity_number)) as file_json:
        json_pose = json.load(file_json)
        file_json.close()
    last_index = len(json_pose)-1
    return json_pose[last_index]


def validate_gesture_face(video_url, identityNumber):
    # os.mkdir("face/quyen")
    cap = cv2.VideoCapture(video_url)
    frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pTime = 0
    complete = False
    count = 0
    pose_json = get_gesture(identityNumber)
    while complete == False and count < frame_number:
        count += 1
        success, img = cap.read()
        # cv2.imwrite("face/quyen/{}.jpg".format(count),img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # print(results.pose_landmarks)
        complete = validate_gesture(imgRGB, pose_json)
        count += 1
        # print(count,frame_number)
        """
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(
                img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                # if id==0: print(id, lm.x)
                if id == 0 and (lm.x-0.7) > 0:
                    complete = True
                cx, cy = int(lm.x * w), int(lm.y * h)
                # cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 255, 255), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)"""

        # cv2.imshow("Image", img)
        # cv2.waitKey(1)
        # img_face_saved = cv2.imread("savedata/face_from_identity/{}.jpg".format(identityNumber))
        # demo = cv2.imread("face/mat.jpg")
        # distance, result = compare_image.main("savedata/face_from_video/{}.jpg".format(count), img_face_saved)
        # print("result", result)
        # print("distance", distance)

    print("complete", complete)
    if not complete:
        # os.remove("savedata/video/{}.mp4".format(identityNumber))
        raise Exception_Handle(name=__name__,
            code=200,
            result=False,
            message="no face return",
            step=3,
            field="file"
        )

    return


def validate_face_vs_identity(identity_number):
    face_identity = cv2.imread(
        "savedata/face_from_identity/{}.jpg".format(identity_number))
    cap = cv2.VideoCapture(
        "savedata/face_from_video/{}.mp4".format(identity_number))
    result = False
    count = 0
    frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while (not result) and count < frame_number:
        _, img = cap.read()
        distance, result = compare_image.main(img, face_identity)
        count+=1
        print(result, distance)

    if not result:
        # os.remove("savedata/face_from_video/{}.mp4".format(identity_number))
        raise Exception_Handle(name=__name__,
            code=200,
            message="compare face fail",
            result=False,
            step=3,
            field="file"
        )
    return 
