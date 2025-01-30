import pytest
import factory
from faker import Faker
import pytest
import uuid
import pytest_asyncio



fake = Faker()

class TaskFactory(factory.Factory):
    class Meta:
        model = dict  # Генерация словаря вместо модели (если нет ORM)

    title = factory.Faker("sentence")
    priority = factory.Iterator([1, 2, 3])

@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get(f"/task/list")
    assert response.status_code == 200
    tasks = response.json()
    for task in tasks:
        assert "id" in task
        assert "title" in task
        assert "priority" in task

@pytest.mark.asyncio
async def test_create_and_delete_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task_data = TaskFactory()

    # Создаём задачу
    create_response = await client.post(f"/task/create_task", json=task_data, headers=headers)
    assert create_response.status_code == 201
    task_id = create_response.json()["task"]["id"]

    # Удаляем задачу
    delete_response = await client.delete(f"/task/delete_task/{task_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Task {task_id} deleted successfully."

@pytest.mark.asyncio
async def test_create_task_without_auth(client):
    task_data = TaskFactory()
    response = await client.post(f"/task/create_task", json=task_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_create_task_without_title(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task_data = {"priority": 1,"text": 'wake up at 8 am'}
    response = await client.post(f"/task/create_task", json=task_data, headers=headers)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

