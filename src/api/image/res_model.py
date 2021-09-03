import enum
from pydantic import BaseModel,Field
from enum import Enum



class Crop_Model(BaseModel):
    result: bool
    base64_string: str

    


