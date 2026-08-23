from pydantic import BaseModel

class VoiceFile(BaseModel):
    voice_note_id:str
    file_path:str
