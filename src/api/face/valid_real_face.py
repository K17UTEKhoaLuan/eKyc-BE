import cv2
import mediapipe as mp
import time
from src.utils.error_handle import Exception_Handle

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
def validate_real_face(video_url):
    cap = cv2.VideoCapture(video_url)
    pTime = 0
    complete = False
    while complete == False:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        # print(results.pose_landmarks)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                if id==0: print(id, lm.x)
                if id==0 and (lm.x-0.7)>0:
                    complete = True
                cx, cy = int(lm.x * w), int(lm.y * h)
                # cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                cv2.putText(img,str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 255, 255), 3)
            

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    print("complete",complete)
    if not complete:
        raise Exception_Handle(
            code=200,
            result=False,
            message="no face return",
            step=3
        )
    return