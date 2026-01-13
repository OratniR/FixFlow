from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

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
    """
    Create a new issue.

    1. Converts content to embedding.
    2. Saves issue and embedding to vector store.
    """
    # Combine title, content, and solution for full context embedding
    full_text = f"{issue.title}\n{issue.content}\n{issue.solution}"
    vector = await embedding_service.embed_text(full_text)

    saved_issue = await vector_service.save_issue(issue, vector)
    return saved_issue


@router.get("/issues/{issue_id}", response_model=IssueRead)
async def get_issue(
    issue_id: str, vector_service: VectorStoreService = Depends(get_vector_service)
) -> IssueRead:
    """Get an issue by ID."""
    issue = await vector_service.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.post("/search", response_model=List[SearchResult])
async def search_issues(
    query: SearchQuery,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorStoreService = Depends(get_vector_service),
) -> List[SearchResult]:
    """
    Semantic search for issues.

    1. Converts query to embedding.
    2. Searches vector store for similar issues.
    """
    query_vector = await embedding_service.embed_text(query.query)
    results = await vector_service.search(query_vector, query.limit, query.filters)
    return results
