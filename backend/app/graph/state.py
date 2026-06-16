from typing import Optional, TypedDict


class AgentState(TypedDict):
    thread_id: str
    user_input: str
    structured_info: Optional[str]  # output nodo Strutturazione
    user_context: Optional[str]
    post_text: Optional[str]  # output nodo Scrittore
    image_url: Optional[str]  # output nodo Diagrammatore
    review_notes: Optional[str]  # output nodo Revisore
    user_approved: Optional[bool]  # human-in-the-loop
