import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from app.models import UserTypeEnum
from app.main import app


@pytest.mark.asyncio
async def test_register_success(prepare_database):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:

        payload = {
            "username": "testuser1",
            "email": "test1@example.com",
            "full_name": "Test User",
            "phone_number": "0812345678",
            "password": "securepass123",
            "user_type": UserTypeEnum.CUSTOMER,
        }
        response = await client.post("/api/auth/register", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
