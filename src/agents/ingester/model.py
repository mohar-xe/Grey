from typing import List

from pydantic import BaseModel, Field


class Source(BaseModel):
    concept_name: str
    raw_text: str  # aggregated scraped content
    sources: List[Source]
    key_facts: List[str]  # bullet-point facts extracted by LLM


class RawKnowledge(BaseModel):
    concept_name: str
    raw_text: str  # aggregated scraped content
    sources: List[Source]
    key_facts: List[str]  # bullet-point facts extracted by LLM


class RelatedConcept(BaseModel):
    id: str
    domain: str
    relation: str  # e.g. "prerequisite", "application", "contrast"


class KnowledgeBlock(BaseModel):
    id: str  # snake_case, matches filename stem
    domain: str  # OKF domain id
    title: str
    tags: List[str]
    aliases: List[str]
    summary: str  # 2-3 sentence abstract
    confidence: float  # 0.0–1.0
    maturity: str  # seed | emerging | established | canonical
    source_quality: str  # anecdotal | web | textbook | peer_reviewed
    sources: List[Source]
    related_concepts: List[RelatedConcept]
    body_markdown: str  # full markdown content below frontmatter
