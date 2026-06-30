from typing import List

from typing_extensions import TypedDict


class IngesterState(TypedDict):
    user_query: str  # forwarded from GlobalState
    query_concepts: List[str]  # concept names extracted from the query
    existing_concepts: List[str]  # already present in OKF
    new_concepts: List[str]  # need to be fetched and ingested
    raw_research: List[dict]  # List[RawKnowledge] from researcher sub-agent
    organized_blocks: List[dict]  # List[KnowledgeBlock] from organizer sub-agent
    written_paths: List[str]  # file paths written to disk by writer sub-agent
    has_new_concepts: bool  # conditional routing flag
