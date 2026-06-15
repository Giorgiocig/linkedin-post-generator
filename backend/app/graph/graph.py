import psycopg
from app.config import settings
from app.graph.nodes import (
    diagrammatore_node,
    revisore_node,
    scrittore_node,
    strutturazione_node,
)
from app.graph.state import AgentState
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, START, StateGraph

_graph = None


async def init_graph():
    global _graph

    builder = StateGraph(AgentState)

    builder.add_node("strutturazione", strutturazione_node)
    builder.add_node("scrittore", scrittore_node)
    builder.add_node("diagrammatore", diagrammatore_node)
    builder.add_node("revisore", revisore_node)

    builder.add_edge(START, "strutturazione")
    builder.add_edge("strutturazione", "scrittore")
    builder.add_edge("scrittore", "diagrammatore")
    builder.add_edge("diagrammatore", "revisore")
    builder.add_edge("revisore", END)

    conn_string = settings.database_url.replace(
        "postgresql+asyncpg://", "postgresql://"
    )
    print(f"FULL CONN STRING: {conn_string}")

    conn = await psycopg.AsyncConnection.connect(conn_string)
    checkpointer = AsyncPostgresSaver(conn)
    await checkpointer.setup()

    _graph = builder.compile(
        checkpointer=checkpointer, interrupt_before=["diagrammatore"]
    )


def get_graph():
    if _graph is None:
        raise RuntimeError("Graph non inizializzato")
    return _graph
