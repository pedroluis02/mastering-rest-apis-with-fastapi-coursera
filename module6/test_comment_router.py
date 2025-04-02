import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_comment(
        async_client: AsyncClient,
        created_post: dict,
        registered_user: dict,
        logged_in_token: str,
):
    body = "Test Comment"

    response = await async_client.post(
        "/comments",
        json={"body": body, "post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
               "id": 1,
               "body": body,
               "post_id": created_post["id"],
               "user_id": registered_user["id"],
           }.items() <= response.json().items()
