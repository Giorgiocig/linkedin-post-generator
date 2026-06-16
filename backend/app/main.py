from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.database import init_db
from app.api.routes import router
from app.graph.graph import init_graph
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_graph()
    yield


app = FastAPI(title="LinkedIn Agent", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_origin_regex="https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
