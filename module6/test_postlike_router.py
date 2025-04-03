import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_like_post(
        async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    response = await async_client.post(
        "/likes",
        json={"post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
