from pydantic import BaseModel
from schemas.enums import MediaType

class ImageFile(BaseModel):
    image_id:str
    file_path:str
