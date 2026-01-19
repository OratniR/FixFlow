import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_api_flow():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        unique_id = str(uuid.uuid4())

        # 1. Create Issue
        payload = {
            "title": f"Timeout Error {unique_id}",
            "content": f"Request timed out after 30s {unique_id}",
            "solution": "Increase timeout to 60s",
            "tags": ["network", "timeout"],
            "metadata": {"env": "prod"},
        }
        response = await ac.post("/api/v1/issues", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        issue_id = data["id"]

        # 2. Get Issue
        response = await ac.get(f"/api/v1/issues/{issue_id}")
        assert response.status_code == 200
        assert response.json()["id"] == issue_id

        # 3. Search Issue
        search_payload = {"query": f"Request timed out {unique_id}", "limit": 5}
        response = await ac.post("/api/v1/search", json=search_payload)
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0
        assert results[0]["id"] == issue_id
        assert "score" in results[0]
