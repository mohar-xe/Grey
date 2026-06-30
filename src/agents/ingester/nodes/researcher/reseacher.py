from datetime import datetime, timezone

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from ...model import RawKnowledge, Source
from ...state import IngesterState
from .prompt import RESEARCHER_PROMPT

_search = TavilySearchResults(max_results=4)


def researcher_node(state: IngesterState) -> dict:
    llm = ChatGroq(model="qwen/qwen3.6-27b")
    raw_research = []

    for concept in state["new_concepts"]:
        # Two searches per concept: definition + research context
        results_def = _search.invoke(f"{concept} definition key properties")
        results_ctx = _search.invoke(f"{concept} current research applications")
        all_results = (results_def or []) + (results_ctx or [])

        sources = [
            Source(
                url=r.get("url", ""),
                title=r.get("title", ""),
                retrieved_at=datetime.now(timezone.utc).isoformat(),
            )
            for r in all_results
            if r.get("url")
        ]
        combined_text = "\n\n".join(r.get("content", "") for r in all_results)

        # LLM extracts key facts from aggregated search content
        resp = llm.invoke(
            [
                SystemMessage(content=RESEARCHER_PROMPT),
                HumanMessage(
                    content=f"CONCEPT: {concept}\n\nRAW CONTENT:\n{combined_text}"
                ),
            ]
        )
        key_facts_raw = resp.content if isinstance(resp.content, str) else ""
        key_facts = [
            f.strip() for f in key_facts_raw.split("\n") if f.strip().startswith("-")
        ]

        raw_research.append(
            RawKnowledge(
                concept_name=concept,
                raw_text=combined_text[:8000],  # truncate to avoid context blowout
                sources=sources,
                key_facts=key_facts,
            ).model_dump()
        )

    return {"raw_research": raw_research}
