from http import client
from fastapi import APIRouter, File, UploadFile, Request
from . import valid_real_face, random_gesture
import os
from .res_model import Gesture_Response, Check_Pose_Response
from src.utils.success_handle import success_return
router = APIRouter()


@router.post("/checkgesture")
async def valid_pose(identityNumber: str, request: Request, file: UploadFile = File(...)):
    # file_name =""
    # file_name+=file.filename
    contents = file.file.read()
    print(type(contents))
    with open("savedata/video/{}.mp4".format(identityNumber), 'wb') as image:
        image.write(contents)
        image.close()
    #     # shutil.copyfileobj(file.file,"a.mp4")
        # nparr = np.fromstring(contents, np.uint8)
        # img_np = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
    #     decoded = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)
        # print(img_np)
    #     print('OpenCV:\n', img_np)
    # cap  = cv2.VideoCapture("20210130_175032.mp4")
    # while(cap.isOpened()):
    #     ret, frame = cap.read()
    #     cv2.imshow('frame',frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()

    valid_real_face.validate_gesture_face(
        "savedata/video/{}.mp4".format(identityNumber), identityNumber)
    os.remove("savedata/video/{}.mp4".format(identityNumber))
    completed, pose_id, pose = random_gesture.next_gesture(
        identityNumber)
    return success_return(
        result=True,
        message="check pose success",
        pose_id=pose_id,
        pose=pose,
        complete=completed,
        client=request.client
    ) if not(completed) else success_return(
        result=True,
        client=request.client,
        message="check pose complete",
        complete=completed,
    )
    return {
        "result": True,
        "pose_id": pose_id,
        "pose": pose,
        "complete": completed
    } if not(completed) else {
        "result": True,
        "complete": completed
    }


@router.post("/gesture", response_model=Gesture_Response)
def get_random_gesture(identityNumber: str):
    pose_id, pose = random_gesture.random_face_gesture(identityNumber)

    return {
        "result": True,
        "pose_id": pose_id,
        "pose": pose
    }


@router.post("/compareface")
async def compare_face(identityNumber: str, request: Request, file: UploadFile = File(...)):
    contents = file.file.read()
    print(type(contents))
    with open("savedata/face_from_video/{}.mp4".format(identityNumber), 'wb') as image:
        image.write(contents)
        image.close()
    valid_real_face.validate_face_vs_identity(identityNumber)
    os.remove("savedata/face_from_video/{}.mp4".format(identityNumber))
    return success_return(
        result=True,
        message="compare face success",
        client=request.client
    )
    return{
        "result": True,
    }
