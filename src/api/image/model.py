from pydantic import BaseModel

class Image(BaseModel):
    image: str
    imageWidth: int
    imageHeight: int
    identityWidth: int
    identityHeight: int