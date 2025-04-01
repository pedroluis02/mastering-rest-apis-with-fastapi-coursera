import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

os.environ["ENV_STATE"] = "test"
from .database import database  # noqa: E402
from .app import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client_m4() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db_m4() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client_m4(client_m4) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client_m4.base_url) as ac:
        yield ac
