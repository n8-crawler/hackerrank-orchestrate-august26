from datetime import datetime
from pydantic import BaseModel
from .enums import ConversationType,MediaType

class IncomingMessage(BaseModel):
    message_id:str
    user_id:str
    conversation_type:ConversationType
    group_id:str|None=None
    business_id:str|None=None
    sender_user_id:str|None=None
    created_at:datetime
    message_text:str| None=""
    media_type:MediaType|None=None
    media_id:str|None=None
    forwarded_count:int
