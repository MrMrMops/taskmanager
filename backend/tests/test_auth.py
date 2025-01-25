import logging

import pytest

logger = logging.getLogger(__name__)

from fastapi import Depends

#
from sqlalchemy.orm import Session



@pytest.mark.asyncio
async def test_register_user(client):
    user_data = {
        "name": "testuser1",
        "password": "strongpassword123"
    }
    global id_user
    response =await client.post("http://127.0.0.1:8000/auth/register", json=user_data)


    id_user = response.json()['id']
    assert 'id' in response.json()
    assert response.status_code == 200

    # assert "access_token" in data

@pytest.mark.asyncio
async def test_login_user(client,):
    global token
    user_data = {
        "username": "testuser",
        "password": "strongpassword123"
    }

    # Отправка данных в формате form-data
    response = await client.post("http://127.0.0.1:8000/auth/login", data=user_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]




@pytest.mark.asyncio
async def test_delete_user(client):

    response = await client.delete(f"http://127.0.0.1:8000/auth/delete_user/{id_user}")
    assert response.status_code == 200

