from pydantic import BaseModel

class Gesture_Response(BaseModel):
    result: bool
    pose_id: int
    pose: str

class Check_Pose_Response(BaseModel):
    result: bool
    pose_id: int
    pose: str
    complete: bool
