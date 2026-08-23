from pydantic import BaseModel, Field

class OutputIds(BaseModel):
    message_id:str
