from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class TaskSpec(BaseModel):
    id: str = Field(..., description="Unique task identifier, e.g. task_1")
    title: str = Field(..., description="Human-readable task title")
    description: str = Field(..., description="What the agent should accomplish")
    designated_agent: str = Field(..., description="Agent name from AGENTS_REGISTRY")
    dependencies: List[str] = Field(
        default_factory=list,
        description="Task IDs that must complete before this task begins",
    )
    priority: Literal["critical", "high", "normal", "low"] = Field(
        default="normal", description="Execution priority hint"
    )


class ExclusionNote(BaseModel):
    agent: str = Field(..., description="Agent name excluded from plan")
    reason: str = Field(..., description="Why this agent is not needed")


class TaskPlan(BaseModel):
    tasks: List[TaskSpec] = Field(..., description="Ordered list of tasks")
    reasoning: str = Field(..., description="Planner's high-level rationale")
    excluded_agents: List[ExclusionNote] = Field(
        default_factory=list, description="Agents not included in this plan and why"
    )
