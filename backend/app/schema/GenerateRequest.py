from pydantic import BaseModel


class GenerateRequest(BaseModel):
    user_input: str
