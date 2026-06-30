from src.agents.planner.graph import build_planner_graph
from src.agents.planner.model import TaskSpec
from src.agents.planner.state import PlannerState
from src.orchestration.state import AgentResult, GlobalState


def run_planner(state: GlobalState, task: TaskSpec) -> AgentResult:
    planner_state = PlannerState(
        user_query=state["user_query"],
        reasoning_trace="",
        task_plan=None,
    )
    graph = build_planner_graph()
    final = graph.invoke(planner_state)
    return AgentResult(
        agent="planner",
        task_id=task["id"],
        status="success",
        output=final["task_plan"]["reasoning"],
        data={"task_plan": final["task_plan"]},
        okf_mutations=[],
    )
