from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from module2.router import comments_table, post_table
from .app import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client_m3() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db_m3() -> AsyncGenerator:
    post_table.clear()
    comments_table.clear()
    yield


@pytest.fixture()
async def async_client_m3(client_m3) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client_m3.base_url) as ac:
        yield ac
