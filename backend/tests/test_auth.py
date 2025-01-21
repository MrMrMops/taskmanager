import pytest

@pytest.mark.asyncio
async def test_register_user(client):
    user_data = {
        "username": "testuser",
        "password": "strongpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_login_user(client):
    user_data = {
        "username": "testuser",
        "password": "strongpassword123"
    }
    client.post("/auth/register", json=user_data)

    response = client.post("/auth/login", data=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data