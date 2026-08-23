from pydantic import BaseModel

class BusinessAccount(BaseModel):
    business_id:str
    display_name:str
    brand_name:str
    category:str
    verified:bool
    official_domain:str |None=None
    domain_used_by_sender:str|None=None
    account_age_days:int
    messages_sent_30d:int
    user_reports_30d:int
    domain_used_by_sender_age_days:int
