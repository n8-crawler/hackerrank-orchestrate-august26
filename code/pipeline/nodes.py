from code.schemas.response import NotificationDecision
from pipeline.dataclass import NotificationState
from agents.notification_router import Router
from services.llmservice import LLMservice

def build_context_node(state:NotificationState):
    state.context = Router().build_context(message_id=state.message_id)
    return state

def image_analyse_node(state:NotificationState):
    if state.context['image']:
        state.image_analysis = LLMservice().analyse_image(state.context['image'].file_path)
    return state
    
def voice_analysis_node(state:NotificationState):
    if state.context['voice']:
        state.voice_analysis = LLMservice().voice_transcript(state.context['voice'].file_path)
    return state

def build_prompt_node(state:NotificationState):
    state.prompt = Router().build_prompt(context=state.context,image_analysis=state.image_analysis,voice_transcript=state.voice_analysis)
    return state

def build_response_node(state:NotificationState):
    state.response = LLMservice().reason(prompt=state.prompt)
    return state

def parser_node(state: NotificationState):
    state.decision = NotificationDecision.model_validate_json(state.response)
    return state