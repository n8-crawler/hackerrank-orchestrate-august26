from datetime import datetime
from pydantic import BaseModel

class GroupMembership(BaseModel):
    group_id:str
    user_id:str
    role:str
    joined_at:datetime
    messages_sent_30d:int
    messages_read_30d:int
    replies_sent_30d:int
    notifications_dismissed_30d:int
    group_muted_by_user:bool
