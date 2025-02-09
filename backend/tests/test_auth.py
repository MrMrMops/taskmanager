import pytest


@pytest.mark.asyncio
async def test_register_user_successfully(client, user_data):

    response = await client.post("/auth/register", json=user_data)
    id_user = response.json()['id']

    assert response.status_code == 200
    assert response.json()['id'] is not None
    response = await client.delete(f"/auth/delete_user/{id_user}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_user(client, log_data):

    response = await client.post("/auth/login", data=log_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_user_with_invalid_credentials(client,):
    user_data = {
        "username": "testuser404",
        "password": "strongpassword123"
    }

    response = await client.post("/auth/login", data=user_data)

    assert response.status_code == 401
    assert response.json()['detail'] == "Invalid username or password"


@pytest.mark.asyncio
async def test_delete_user404(client):
    invalid_user_id = -1
    response = await client.delete(f"/auth/delete_user/{invalid_user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == f"Task with ID {invalid_user_id} not found."
