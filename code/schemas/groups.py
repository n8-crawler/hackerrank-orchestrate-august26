from datetime import datetime
from pydantic import BaseModel

class Group(BaseModel):
    group_id:str
    group_name:str
    group_type:str
    member_count:int
    admin_count:int
    created_at:datetime
    messages_30d:int
