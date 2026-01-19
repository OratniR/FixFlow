from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Literal

from app.schemas import IssueCreate, IssueRead, SearchQuery, SearchResult
from app.services.base import VectorStoreService, EmbeddingService
from app.api.deps import get_embedding_service, get_vector_service

router = APIRouter()


@router.post("/issues", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
async def create_issue(
    issue: IssueCreate,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorStoreService = Depends(get_vector_service),
) -> IssueRead:
    """Create a new issue."""
    full_text = f"{issue.title}\n{issue.content}\n{issue.solution}"
    vector = await embedding_service.embed_text(full_text)
    saved_issue = await vector_service.save_issue(issue, vector)
    return saved_issue


@router.get("/issues/trending", response_model=List[IssueRead])
async def get_trending_issues(
    limit: int = 10, vector_service: VectorStoreService = Depends(get_vector_service)
) -> List[IssueRead]:
    """Get trending issues based on popularity and recency."""
    return await vector_service.get_trending(limit)


@router.get("/issues/{issue_id}", response_model=IssueRead)
async def get_issue(
    issue_id: str, vector_service: VectorStoreService = Depends(get_vector_service)
) -> IssueRead:
    """Get an issue by ID."""
    issue = await vector_service.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.post("/issues/{issue_id}/feedback")
async def send_feedback(
    issue_id: str,
    type: Literal["view", "useful"] = Query(..., description="Type of feedback"),
    vector_service: VectorStoreService = Depends(get_vector_service),
) -> dict:
    """
    Record feedback (view or useful vote).
    Agents should call this when they use an issue to solve a problem.
    """
    # Verify issue exists
    issue = await vector_service.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    await vector_service.increment_counter(issue_id, type)
    return {"status": "success", "message": f"Recorded {type} for issue {issue_id}"}


@router.post("/search", response_model=List[SearchResult])
async def search_issues(
    query: SearchQuery,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorStoreService = Depends(get_vector_service),
) -> List[SearchResult]:
    """Semantic search for issues."""
    query_vector = await embedding_service.embed_text(query.query)
    results = await vector_service.search(query_vector, query.limit, query.filters)
    return results
