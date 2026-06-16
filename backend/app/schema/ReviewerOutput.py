from typing import Literal
from pydantic import BaseModel

class ReviewerOutput(BaseModel):
    esito: Literal["APPROVATO", "DA_RIVEDERE"]
    feedback: str