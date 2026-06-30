from langgraph.graph import END, START, StateGraph

from .nodes.check import check_node
from .nodes.organizer.organizer import organizer_node
from .nodes.researcher.researcher import researcher_node
from .nodes.writer.writer import writer_node
from .state import IngesterState


def route_after_check(state: IngesterState) -> str:
    return "researcher" if state["has_new_concepts"] else END


def build_ingester_graph():
    workflow = StateGraph(IngesterState)
    workflow.add_node("check", check_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("organizer", organizer_node)
    workflow.add_node("writer", writer_node)

    workflow.add_edge(START, "check")
    workflow.add_conditional_edges(
        "check",
        route_after_check,
        {
            "researcher": "researcher",
            END: END,
        },
    )
    workflow.add_edge("researcher", "organizer")
    workflow.add_edge("organizer", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
