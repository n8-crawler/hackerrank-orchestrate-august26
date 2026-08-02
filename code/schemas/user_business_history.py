from datetime import datetime
from pydantic import BaseModel

class UserBusinessHistory(BaseModel):
    user_id:str
    business_id:str
    why_user_knows_account:str
    last_activity_at:datetime|None=None
    allows_promotions:bool
    promotions_opted_out_at:datetime|None=None
    activity_count_180d:int
    messages_opened_30d:int
    messages_dismissed_30d:int
    messages_replied_30d:int
    last_reply_at:datetime|None=None
