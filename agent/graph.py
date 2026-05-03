from langgraph.graph import StateGraph, END
from agent.state import ReviewState
from agent.nodes import (
    router,
    read_file_node,
    use_inline_node,
    review_code_node,
    format_output_node,
)

def route_condition(state: ReviewState) -> str:
    return state.get("route", "inline")

def build_graph() -> StateGraph:
    graph = StateGraph(ReviewState)

    # ── register nodes ────────────────────────────────────────────────────────
    graph.add_node("router",        router)
    graph.add_node("read_file",     read_file_node)
    graph.add_node("use_inline",    use_inline_node)
    graph.add_node("review_code",   review_code_node)
    graph.add_node("format_output", format_output_node)

    # ── entry point ───────────────────────────────────────────────────────────
    graph.set_entry_point("router")

    # ── conditional edge: router → read_file | use_inline ────────────────────
    graph.add_conditional_edges(
        "router",
        route_condition,
        {
            "file":   "read_file",
            "inline": "use_inline",
        }
    )

    # ── linear edges ──────────────────────────────────────────────────────────
    graph.add_edge("read_file",     "review_code")
    graph.add_edge("use_inline",    "review_code")
    graph.add_edge("review_code",   "format_output")
    graph.add_edge("format_output", END)

    return graph.compile()