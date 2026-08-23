from pydantic import BaseModel

class UserProfile(BaseModel):
    user_id:str
    do_not_disturb_window:str
    messages_opened_30d:int
    messages_replied_30d:int
    notifications_dismissed_30d:int
    messages_reported_30d:int
