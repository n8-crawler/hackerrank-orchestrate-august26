from code.schemas.response import NotificationDecision
from schemas.enums import MediaType
from schemas.notifications import NotificationDesicion
from services.llmservice import LLMservice
from agents.retrival import Retriver
class Router:
    def __init__(self,retriver:Retriver,llm:LLMservice):
        self.retriver = retriver
        self.llm = llm

    def build_context(self,message_id:str)->dict:
        message = self.retriver.get_message(message_id=message_id)
        if message is None:
            raise ValueError(f'No message found for {message_id}')
        
        return {
            'message':message,
            'user':self.retriver.get_user(user_id=message.user_id),
            'business':self.retriver.get_business(business_id=message.business_id),
            'group':self.retriver.get_group(group_id=message.group_id),
            'group_member':self.retriver.get_group_members(group_id=message.group_id,user_id=message.user_id),
            'image':self.retriver.get_images(media_id=message.media_id) if message.media_type == MediaType.IMAGE  else None,
            'voice':self.retriver.get_voice_notes(media_id=message.media_id) if message.media_type == MediaType.VOICE else None,
            'user_business_history':self.retriver.get_user_business_history(user_id=message.user_id,business_id=message.business_id),
            'message_history':self.retriver.get_message_history(user_id=message.user_id),
            'message_events':self.retriver.get_message_events(user_id=message.user_id,message_id=message.message_id),
            'notification_summary':self.retriver.get_notification_summary(user_id=message.user_id)
        }

    def build_prompt(self,context:dict,image_analysis:str|None,voice_transcript:str|None)->str:
        message = context["message"]
        user = context["user"]
        group = context["group"]
        group_member = context["group_member"]
        business = context["business"]
        user_business_history = context["user_business_history"]
        user_history = context["message_history"]
        message_events = context["message_events"]
        notification = context["notification_summary"]
        image = context["image"]
        voice = context["voice"]

        sections = []

        sections.append(f"""
            ============CURRENT MESSAGE===========
            Message Id : {message.message_id}
            Conversation Type : {message.conversation_type}
            Created At : {message.created_at}
            Message Text : {message.message_text}
            Media Type : {message.media_type}
            Forwarded Count : {message.forwarded_count}
        """
        )
        sections.append(f"""
        ==============USER==============
        User Id : {user.user_id}
        Message ID : {user.message_id}
        Quiet Hours : {user.do_not_disturb_window}
        Messages Opened in last 30 days: {user.messages_opened_30d}
        Messages replied in last 30 days: {user.messages_replied_30d}
        Messages dismissed in last 30 days: {user.notifications_dismissed_30d}
        Messages reported in last 30 days: {user.messages_reported_30d}
        """)

        if group:
            sections.append(f"""
            Group Name : {group.group_name}
            Group Type : {group.group_type}
            Number of Members : {group.member_count}
            Messaged received in last 30 days : {group.messages_30d}
         """)

        if business:
            sections.append(f"""
            ===============BUSINESS==============
            Business Id : {business.business_id}
            Business Name : {business.display_name}
            Brand Name : {business.brand_name}
            Category : {business.category}
            Verified : {business.verified}
            Official Domain : {business.official_domain}
            Domain Used by Sender : {business.domain_used_by_sender}
            Number of User Reported : {business.user_reports_30d}
         """)

        if user_business_history:
            sections.append(f"""
            ===========USER BUSINESS HISTORY================
            Business Id : {user_business_history.business_id}
            Business User Relationship : {user_business_history.why_user_knows_account}
            Allow Promitional Messages : {user_business_history.allows_promotions}
            Activity Count in last 180 days : {user_business_history.activity_count_180d}
         """)

        if user_history:
            sections.append(f"""
            ===============User OLD MESSAGE HISTORY==============
            User Id : {user_history.user_id}
            Messages Id : {user_history.message_id}
            Business ID : {user_history.business_id}
            Conversation Type : {user_history.conversation_type}
            Message Text : {message.message_text}
            Media Type : {message.media_type}
        """)

        if message_events:
            sections.append(f"""
            User Id : {message_events.user_id}
            Message ID : {message_events.message_id}
            Message Read : {message_events.message_opened}
            Message Replied : {message_events.message_replied}
            Message Reported : {message_events.message_reported}
             """)

        if image:
            sections.append(f"""
            ========== IMAGE ANALYSIS ==========
            Analysed Image : {image_analysis}
            """)

        if voice:
            sections.append(f"""
            ========== VOICE MESSAGES ANALYSIS==========
            Transcribed Voice Message : {voice_transcript}
            """)
        sections.append("""
            ========== TASK ==========
            You are an AI Notification Router.
            Analyze the current WhatsApp message using all provided context.
            Determine:
            1. action:

                notify
                digest
                mute

            2. message_type:

                personal
                urgent
                event
                payment
                business_update
                promotion
                greeting
                forward
                spam
                scam
                unknown

            Return ONLY valid JSON.

            {{
                "message_id":"",
                "action":"",
                "message_type":"",
                "reason":"",
                "confidence":0.0,
                "evidence_message_ids":[]
            }}

            Do not explain.
            Do not use markdown.
            Return JSON only.
            """)

        return "\n".join(sections)


    def build_route(self,message_id:str):
        context = self.build_context(message_id)

        # image processing.....
        image_analysis = None
        if context['image']:
            image_analysis = self.llm.analyse_image(context['image'].file_path)

        # voice processing.....
        voice_transcript=None
        if context['voice']:
            voice_transcript = self.llm.voice_transcript(context['voice'].file_path)

        prompt = self.build_prompt(context,image_analysis,voice_transcript)

        response = self.llm.reason(prompt)
        print(f"LLM Response : {response}")
        return NotificationDecision.model_validate_json(response)