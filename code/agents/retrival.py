from schemas.notifications import NotificationDesicion
from schemas.incoming_message import IncomingMessage
from services.llmservice import LLMservice
from services.dataloader import DataLoader
from schemas.incoming_message import IncomingMessage
from schemas.users import UserProfile
from schemas.groups import Group
from schemas.group_membership import GroupMembership
from schemas.business import BusinessAccount
from schemas.user_business_history import UserBusinessHistory
from schemas.message_events import MessageEvents
from schemas.images import ImageFile
from schemas.voice_notes import VoiceFile
from schemas.daily_notification import DailyNotification

class Retriver:
    def __init__(self):
        self.llm = LLMservice()
        self.data = DataLoader()

    def get_message(self,message_id:str)->IncomingMessage|None:
        for message in self.data.messages:
            if message.message_id == message_id:
                return message
        return None

    def get_user(self,user_id:str)->UserProfile | None:
        for user in self.data.users:
            if user.user_id == user_id:
                return user
        return None

    def get_business(self,business_id:str)->BusinessAccount|None:
        for business_account in self.data.business_accounts:
            if business_account.business_id == business_id:
                return business_account
        return None

    def get_group(self,group_id:str)->Group|None:
        for group in self.data.groups:
            if group.group_id == group_id:
                return group
        return None

    def get_group_members(self,group_id:str,user_id:str)->GroupMembership|None:
        for group_members in self.data.group_members:
            if group_members.group_id == group_id and group_members.user_id == user_id:
                return group_members
        return None

    def get_images(self,media_id:str)->ImageFile|None:
        for image in self.data.images:
            if image.image_id == media_id:
                return image
        return None

    def get_user_business_history(self, user_id:str,business_id:str)->UserBusinessHistory|None:
        for business_history in self.data.user_business_history:
            if business_history.user_id == user_id and business_history.business_id == business_id:
                return business_history
        return None

    def get_message_history(self,user_id:str)->list[IncomingMessage]|None:
            message_history = []
            for message in self.data.message_history:
                if message.user_id == user_id:
                    message_history.append(message)
            return message_history if len(message_history)>0 else None

    def get_voice_notes(self,voice_id:str)->VoiceFile|None:
        for voice in self.data.voice_notes:
            if voice.voice_note_id == voice_id:
                return voice
        return None

    def get_message_events(self,user_id:str,message_id:str)->list[MessageEvents]|None:
        message_events = []
        for msg_event in self.data.message_events:
            if msg_event.user_id == user_id and msg_event.message_id==message_id:
                message_events.append(msg_event)
        return message_events if len(message_events) > 0 else None
    
    def get_notification_summary(self,user_id:str)->DailyNotification|None:
        for notification in self.data.daily_notification_summary:
            if notification.user_id == user_id:
                return notification
        return None
