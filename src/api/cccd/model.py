from pydantic import BaseModel

class Identity(BaseModel):
    name: str
    identityNumber: str
    address: str
    birthday: str
    frontside: str
    backside: str
    code: int
    sex: str
