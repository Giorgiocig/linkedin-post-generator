from pydantic import BaseModel


class GenerateResponse(BaseModel):
    thread_id: str
    post_text: str
    review_notes: str
