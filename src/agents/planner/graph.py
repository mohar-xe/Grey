from agents.planner.nodes.plan import plan_node
from agents.planner.state import PlannerState
from langgraph.graph import END, START, StateGraph


def build_planner_graph():
    workflow = StateGraph(PlannerState)
    workflow.add_node("plan", plan_node)
    workflow.add_edge(START, "plan")
    workflow.add_edge("plan", END)
    return workflow.compile()
