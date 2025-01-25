import pytest


@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get("http://127.0.0.1:8000/task/list")
    assert response.status_code == 200
    tasks = response.json()
   # print(tasks)
    assert isinstance(tasks, list)

@pytest.mark.asyncio
async def test_delete_task(client):

    user_data = {
        "name": "testuser1",
        "password": "strongpassword123"
    }
    log_data = {
        "username": "testuser1",
        "password": "strongpassword123"
    }

    task_data = {"title": "Task to delete", "priority": 1}
    register = await client.post("http://127.0.0.1:8000/auth/register", json=user_data)
    assert 'id' in register.json()
    register_id = register.json()['id']
    auth = await client.post("http://127.0.0.1:8000/auth/login", data=log_data)
    assert "access_token" in auth.json()
    auth = auth.json()["access_token"]
    response = await client.post("http://127.0.0.1:8000/task/create_task", json=task_data, headers=({"Authorization": f"Bearer {auth}"}))
    await client.delete(f"http://127.0.0.1:8000/auth/delete_user/{register_id}")
    assert 'id' in response.json()['task']
    task_id = response.json()['task']['id']


    # Удаляем задачу
    delete_response = await client.delete(f"http://127.0.0.1:8000/task/delete_task/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Task {task_id} deleted successfully."
