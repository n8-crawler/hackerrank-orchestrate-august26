from datetime import date
from pydantic import BaseModel

class DailyNotification(BaseModel):
    user_id:str
    date:date
    notifications_sent:int
    notifications_dismissed:int
