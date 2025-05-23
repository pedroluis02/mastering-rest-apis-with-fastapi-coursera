import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client_m3: AsyncClient) -> dict:
    response = await async_client_m3.post(
        "/posts",
        json={"body": body},
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client_m3: AsyncClient):
    return await create_post("Test Post", async_client_m3)


@pytest.fixture()
async def created_comment(async_client_m3: AsyncClient, created_post: dict):
    response = await async_client_m3.post(
        "/comments",
        json={"body": "Test Comment", "post_id": created_post["id"]},
    )
    return response.json()


@pytest.mark.anyio
async def test_create_post(async_client_m3: AsyncClient):
    body = "Test Post"
    response = await async_client_m3.post(
        "/posts",
        json={"body": body},
    )
    assert response.status_code == 201
    assert {"id": 0, "body": "Test Post"}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client_m3: AsyncClient):
    response = await async_client_m3.post(
        "/posts",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client_m3: AsyncClient, created_post: dict):
    response = await async_client_m3.get("/posts")
    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(
        async_client_m3: AsyncClient,
        created_post: dict,
):
    body = "Test Comment"

    response = await async_client_m3.post(
        "/comments",
        json={"body": body, "post_id": created_post["id"]},
    )
    assert response.status_code == 201
    assert {
               "id": 0,
               "body": body,
               "post_id": created_post["id"],
           }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
        async_client_m3: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m3.get(f"/posts/{created_post['id']}/comments")
    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_post_with_comments(
        async_client_m3: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m3.get(f"/posts/{created_post['id']}")
    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
        async_client_m3: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m3.get("/posts/2")
    assert response.status_code == 404
