from enum import Enum

class ConversationType(str, Enum):
    PERSONAL="personal"
    GROUP="group"
    BUSINESS="business"

class MediaType(str, Enum):
    IMAGE="image"
    VOICE="voice"

class MessageAction(str, Enum):
    NOTIFY="notify"
    DIGEST="digest"
    MUTE="mute"

class MessageCategory(str, Enum):
    PERSONAL="personal"
    URGENT="urgent"
    EVENT="event"
    PAYMENT="payment"
    BUSINESS_UPDATE="business_update"
    PROMOTION="promotion"
    GREETING="greeting"
    FORWARD="forward"
    SPAM="spam"
    SCAM="scam"
    UNKNOWN="unknown"
