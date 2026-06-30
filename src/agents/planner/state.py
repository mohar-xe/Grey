from typing import Optional

from typing_extensions import TypedDict

from .model import TaskPlan


class PlannerState(TypedDict):
    user_query: str  # original query, immutable
    reasoning_trace: str  # planner's CoT before committing to plan
    task_plan: Optional[TaskPlan]
