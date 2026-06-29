from langgraph.graph import END, START, StateGraph
from orchestration.checkpoints import get_checkpointer
from orchestration.router import route_next_task
from orchestration.state import GlobalState


def build_grey_graph():
    workflow = StateGraph(GlobalState)

    # ── Agent node registry ──
    agent_nodes = {
        "planner": planner_node,
        "ingester": ingester_node,  # wraps sub-graph internally
        "connector": connector_node,
        "contemplator": contemplator_node,
        "innovator": innovator_node,
        "curator": curator_node,
        "contradictor": contradictor_node,
        "reporter": reporter_node,
    }

    # 1. Register all nodes
    for name, fn in agent_nodes.items():
        workflow.add_node(name, fn)

    # 2. Entry: START → planner
    workflow.add_edge(START, "planner")

    # 3. Build routing map (all possible targets + END)
    routing_map = {name: name for name in agent_nodes if name != "planner"}
    routing_map["__end__"] = END

    # 4. Planner routes to first task via conditional edge
    workflow.add_conditional_edges("planner", route_next_task, routing_map)

    # 5. Every non-planner agent routes back to supervisor router
    for agent_name in agent_nodes:
        if agent_name != "planner":
            workflow.add_conditional_edges(agent_name, route_next_task, routing_map)

    # 6. Compile with checkpointer
    return workflow.compile(checkpointer=get_checkpointer())


def make_agent_node(agent_name: str, agent_fn):
    """Wraps any agent callable into a GlobalState-compatible node."""

    def node(state: GlobalState) -> dict:
        # 1. Find the current task for this agent
        completed = set(state.get("completed_tasks", []))
        task = next(
            t
            for t in state["task_plan"]["tasks"]
            if t["designated_agent"] == agent_name and t["id"] not in completed
        )

        # 2. Execute agent (passes full state; agent reads what it needs)
        result: AgentResult = agent_fn(state, task)

        # 3. Return GlobalState updates
        updates = {
            "completed_tasks": [task["id"]],
            "agent_results": [result],
            "current_task_id": task["id"],
            "current_phase": agent_name + "ing",  # rough phase label
        }

        # 4. Merge agent-specific outputs
        if agent_name == "ingester":
            updates["ingested_concepts"] = result["data"].get("concept_ids", [])
        elif agent_name == "connector":
            updates["connections"] = result["data"].get("connections", [])
        elif agent_name == "innovator":
            updates["innovations"] = result["data"].get("innovations", [])
        elif agent_name == "contradictor":
            updates["contradiction_verdicts"] = result["data"].get("verdicts", [])
            updates["approved_connections"] = [
                v for v in result["data"].get("verdicts", []) if v.get("survived")
            ]
        elif agent_name == "reporter":
            updates["final_report"] = result["output"]
            updates["current_phase"] = "complete"

        return updates

    return node
