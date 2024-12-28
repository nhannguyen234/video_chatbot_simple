from pydantic import BaseModel

class Message(BaseModel):
    id: str
    question: str
    video_url: str = ''
    image_url: str = ''