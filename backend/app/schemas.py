from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IssueBase(BaseModel):
    """Base model for Issue shared properties."""

    title: str = Field(..., description="Brief summary of the issue")
    content: str = Field(..., description="Detailed description and logs (Markdown)")
    solution: str = Field(
        ..., description="The working fix and its reasoning (Markdown)"
    )
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional context (env, language, etc)"
    )


class IssueCreate(IssueBase):
    """Schema for creating a new issue."""

    pass


class IssueRead(IssueBase):
    """Schema for reading an issue."""

    id: str
    created_at: datetime
    updated_at: datetime
    view_count: int = 0
    useful_count: int = 0


class SearchQuery(BaseModel):
    """Schema for semantic search query."""

    query: str = Field(..., description="Natural language query")
    limit: int = Field(default=5, ge=1, le=20)
    filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters")


class SearchResult(IssueRead):
    """Schema for search results with score."""

    score: float = Field(..., description="Similarity score")
