import operator
from typing import Annotated, Any, Dict, List, Literal, Optional, TypedDict

from langgraph.graph.message import add_messages


class TaskPlan(TypedDict):
    """Structured output from the planner agent."""

    tasks: List["TaskSpec"]  # ordered list of tasks to execute
    reasoning: str  # planner's rationale for this plan
    excluded_agents: List["ExclusionNote"]  # agents excluded and why


class TaskSpec(TypedDict):
    """Single task within the plan."""

    id: str  # unique task id, e.g. "task_1"
    title: str  # human-readable task title
    description: str  # what the agent should accomplish
    designated_agent: str  # agent name from AGENTS_REGISTRY
    dependencies: List[str]  # task ids that must complete first
    priority: Literal["critical", "high", "normal", "low"]  # execution priority


class ExclusionNote(TypedDict):
    """Why an agent was excluded from the plan."""

    agent: str  # agent name
    reason: str  # rationale for exclusion


class AgentResult(TypedDict):
    """Standardized output from any agent."""

    agent: str  # which agent produced this
    task_id: str  # which task this fulfills
    status: Literal["success", "partial", "rejected"]  # outcome
    output: str  # primary textual output
    data: Dict[str, Any]  # structured payload (agent-specific)
    okf_mutations: List[str]  # list of OKF file paths written/modified


class GlobalState(TypedDict):
    # ── Conversation ──
    messages: Annotated[list, add_messages]  # full message history for tracing
    user_query: str  # original user query, immutable after set

    # ── Planning ──
    task_plan: Optional[TaskPlan]  # planner output; None until planner runs
    current_task_id: Optional[str]  # task currently being executed
    completed_tasks: Annotated[List[str], operator.add]  # task ids completed so far

    # ── Agent outputs ──
    agent_results: Annotated[
        List[AgentResult], operator.add
    ]  # accumulated results from all agents

    # ── Memory context ──
    memory_snapshot: Dict[str, Any]  # OKF data retrieved for this query
    ingested_concepts: List[str]  # concept ids ingested during this run

    # ── Connection / Innovation ──
    connections: List[Dict[str, Any]]  # connections found by connector/innovator
    innovations: List[Dict[str, Any]]  # novel bisociations from innovator

    # ── Quality gate ──
    contradiction_verdicts: List[
        Dict[str, Any]
    ]  # contradictor pass/fail per connection
    approved_connections: List[Dict[str, Any]]  # connections that survived contradictor

    # ── Final output ──
    final_report: Optional[str]  # reporter's rendered output
    current_phase: Literal[  # human-readable phase label
        "planning",
        "ingesting",
        "connecting",
        "innovating",
        "contemplating",
        "curating",
        "contradicting",
        "reporting",
        "complete",
    ]
