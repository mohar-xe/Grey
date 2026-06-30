import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from src.memory.vault import MemoryVault

from ..state import IngesterState

_CONCEPT_EXTRACT_PROMPT = """Extract the main named concepts, entities, or topics
from the user query. Return them as a comma-separated list. No explanation.
"""


def check_node(state: IngesterState) -> dict:
    # 1. Extract concept names from the query using Haiku
    llm = ChatGroq(model="qwen/qwen3.6-27b")
    resp = llm.invoke(
        [
            SystemMessage(content=_CONCEPT_EXTRACT_PROMPT),
            HumanMessage(content=state["user_query"]),
        ]
    )
    raw = resp.content if isinstance(resp.content, str) else ""
    query_concepts = [
        c.strip().lower().replace(" ", "_") for c in raw.split(",") if c.strip()
    ]

    # 2. Check OKF index for existing concepts
    vault = MemoryVault()
    index = vault.read_index()
    all_known = {
        c for domain in index.get("domains", []) for c in domain.get("concept_ids", [])
    }

    existing = [c for c in query_concepts if c in all_known]
    new = [c for c in query_concepts if c not in all_known]

    return {
        "query_concepts": query_concepts,
        "existing_concepts": existing,
        "new_concepts": new,
        "has_new_concepts": bool(new),
    }
