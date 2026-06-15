from pydantic import BaseModel


class ResumeRequest(BaseModel):
    thread_id: str
    post_text: str  # testo modificato dall'utente
