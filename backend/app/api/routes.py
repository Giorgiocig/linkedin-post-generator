from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.graph import get_graph
import uuid

router = APIRouter(prefix="/api")


class GenerateRequest(BaseModel):
    user_input: str


class ResumeRequest(BaseModel):
    thread_id: str
    post_text: str


class GenerateResponse(BaseModel):
    thread_id: str
    post_text: str
    review_notes: str


class ResumeResponse(BaseModel):
    thread_id: str
    post_text: str
    image_url: str
    review_notes: str


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    thread_id = str(uuid.uuid4())
    graph = get_graph()
    config = {"configurable": {"thread_id": thread_id}}

    state = await graph.ainvoke(
        {"user_input": request.user_input, "thread_id": thread_id}, config=config
    )

    return GenerateResponse(
        thread_id=thread_id,
        post_text=state["post_text"],
        review_notes=state.get("review_notes", ""),
    )


@router.post("/resume", response_model=ResumeResponse)
async def resume(request: ResumeRequest):
    graph = get_graph()
    config = {"configurable": {"thread_id": request.thread_id}}

    # prima aggiorna il post_text nello state
    await graph.aupdate_state(config, {"post_text": request.post_text})

    # poi riprendi dall'interrupt passando None
    state = await graph.ainvoke(None, config=config)

    return ResumeResponse(
        thread_id=request.thread_id,
        post_text=state.get("post_text", ""),
        image_url=state.get("image_url", ""),
        review_notes=state.get("review_notes", ""),
    )
