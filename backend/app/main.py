from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.database import init_db
from app.api.routes import router
from app.graph.graph import init_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_graph()
    yield


app = FastAPI(title="LinkedIn Agent", lifespan=lifespan)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
