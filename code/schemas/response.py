from pydantic import BaseModel
from .enums import MessageAction,MessageCategory

class NotificationDecision(BaseModel):
    message_id:str
    action:MessageAction
    message_type:MessageCategory
    reason:str
    confidence:float
    evidence_message_ids:list[str]=[]
