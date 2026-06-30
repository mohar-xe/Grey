from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from ..model import TaskPlan
from ..prompt import PLANNER_SYSTEM_PROMPT
from ..state import PlannerState


def plan_node(state: PlannerState) -> dict:
    llm = ChatGroq(model="qwen/qwen3.6-27b").with_structured_output(TaskPlan)
    plan: TaskPlan = llm.invoke(
        [
            SystemMessage(content=PLANNER_SYSTEM_PROMPT),
            HumanMessage(content=state["user_query"]),
        ]
    )
    return {
        "task_plan": plan.model_dump(),
        "reasoning_trace": plan.reasoning,
    }
