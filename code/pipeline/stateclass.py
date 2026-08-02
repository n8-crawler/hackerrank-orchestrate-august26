from dataclasses import dataclass
from schemas.notifications import NotificationDesicion
@dataclass
class NotificationState:
    message_id : str
    prompt : str | None=None
    image_analysis:str | None=None
    voice_analysis: str | None=None
    context: dict | None=None
    response : str | None=None
    decision : NotificationDesicion | None=None