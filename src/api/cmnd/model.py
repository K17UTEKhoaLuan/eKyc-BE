from app import frontside
from pydantic import BaseModel

class Identity(BaseModel):
    name: str
    name: str
    identityNumber: str
    address: str
    birthday: str
    # frontside: str
    # backside: str