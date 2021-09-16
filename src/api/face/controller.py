from fastapi import APIRouter, File, UploadFile
from . import valid_real_face
import os
router = APIRouter()


@router.post("/uploadvideo")
async def create_upload_file(name: str,file: UploadFile = File(...)):
    # file_name =""
    # file_name+=file.filename
    contents = file.file.read()
    print(type(contents))
    with open("{}.mp4".format(name), 'wb') as image:
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
    valid_real_face.validate_real_face("{}.mp4".format(name))
    os.remove("{}.mp4".format(name))
    return {
        "result": True,
        "message": "Upload video success"
    }

@router.get("/gesture")
def random_gesture():
    return