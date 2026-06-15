from pydantic import BaseModel


class ResumeResponse(BaseModel):
    thread_id: str
    post_text: str
    image_url: str
    review_notes: str
