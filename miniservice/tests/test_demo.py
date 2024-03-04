# test_person_router.py

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import FastAPI
from unittest.mock import AsyncMock
from app.routers.demo import router  # Adjust the import path as necessary


# Fixture to mock Redis dependency
@pytest.fixture
def mock_redis_dependency(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.routers.demo.get_redis_cache", mock)  # Corrected path
    return mock


# Fixture to initialize FastAPI app with the router
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app  # Return the app directly


# Test the /populate/ endpoint
@pytest.mark.asyncio
async def test_populate_redis(app, mock_redis_dependency):
    async with AsyncClient(
        app=app, base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:  # Updated usage
        response = await ac.post(
            "/person/populate/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "age": 30,
            },
        )
    assert response.status_code == 200
    assert "Data successfully saved to Redis" in response.json()["message"]
    mock_redis_dependency.assert_awaited()  # Ensure our mock was awaited


# Test the /retrieve/ endpoint
@pytest.mark.asyncio
async def test_retrieve_redis(app, mock_redis_dependency):
    # Mocking Redis get method to return a person object
    mock_redis_dependency.return_value.get.return_value = '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "age": 30}'.encode()

    async with AsyncClient(
        app=app, base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:  # Updated usage
        response = await ac.get("/person/retrieve/", params={"hash": "somehash"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    mock_redis_dependency.assert_awaited()  # Ensure our mock was awaited
