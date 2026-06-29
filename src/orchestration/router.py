# src/orchestration/router.py
from typing import Literal

from orchestration.state import GlobalState

VALID_AGENTS = {
    "ingester",
    "connector",
    "contemplator",
    "innovator",
    "curator",
    "contradictor",
    "reporter",
}


def route_next_task(state: GlobalState) -> str:
    """Finds the next executable task whose dependencies are all met."""
    task_plan = state.get("task_plan")
    completed = set(state.get("completed_tasks", []))

    if not task_plan or not task_plan["tasks"]:
        return "__end__"
    for task in task_plan["tasks"]:
        task_id = task["id"]
        if task_id in completed:
            continue
        deps = set(task.get("dependencies", []))
        if deps.issubset(completed):
            agent = task["designated_agent"]
            if agent in VALID_AGENTS:
                return agent
            # Unknown agent → skip task, mark done, re-route
            continue

    return "__end__"
