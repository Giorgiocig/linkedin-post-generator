from pydantic import BaseModel

class ReviewerOutput(BaseModel):
    esito: str
    feedback: str