from pydantic import BaseModel

class MessageEvents(BaseModel):
    user_id:str
    message_id:str
    message_opened:bool
    message_replied:bool
    reaction_time_minutes:int|None=None
    notification_dismissed:bool
    muted_after_message:bool
    message_reported:bool
