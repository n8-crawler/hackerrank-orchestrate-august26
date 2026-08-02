from pydantic import BaseModel, Field

from schemas.enums import MessageAction, MessageCategory

class NotificationDesicion(BaseModel):
    message_id : str
    action : MessageAction
    message_type: MessageCategory
    reason : str
    confidence: float = Field(ge=0,le=1)
    evidence_message_id:list[str]=Field(default_factory=list)
    