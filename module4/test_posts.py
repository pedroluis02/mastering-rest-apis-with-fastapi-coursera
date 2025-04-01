import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client_m4: AsyncClient) -> dict:
    response = await async_client_m4.post("/posts", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client_m4: AsyncClient) -> dict:
    response = await async_client_m4.post(
        "/comments", json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client_m4: AsyncClient):
    return await create_post("Test Post", async_client_m4)


@pytest.fixture()
async def created_comment(async_client_m4: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", created_post["id"], async_client_m4)


@pytest.mark.anyio
async def test_create_post(async_client_m4: AsyncClient):
    body = "Test Post"

    response = await async_client_m4.post("/posts", json={"body": body})

    assert response.status_code == 201
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client_m4: AsyncClient):
    response = await async_client_m4.post("/posts", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client_m4: AsyncClient, created_post: dict):
    response = await async_client_m4.get("/posts")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client_m4: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client_m4.post(
        "/comments", json={"body": body, "post_id": created_post["id"]}
    )
    assert response.status_code == 201
    assert {
               "id": 1,
               "body": body,
               "post_id": created_post["id"],
           }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
        async_client_m4: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m4.get(f"/posts/{created_post['id']}/comments")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_post_empty(
        async_client_m4: AsyncClient, created_post: dict
):
    response = await async_client_m4.get(f"/posts/{created_post['id']}/comments")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(
        async_client_m4: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m4.get(f"/posts/{created_post['id']}")

    assert response.status_code == 200
    assert response.json() == {"post": created_post, "comments": [created_comment]}


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
        async_client_m4: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client_m4.get("/posts/2")
    assert response.status_code == 404
