import pytest

@pytest.mark.asyncio
async def test_create_task(client):
    payload = {
        "title": "Test Task",
        "text": "This is a test task",
        "priority": 1
    }
    response = await client.post("/task/create_task", json=payload)
    assert response.status_code == 200
    assert response.json()["message"]["title"] == "Test Task"

@pytest.mark.asyncio
async def test_get_tasks(client):
    response = client.get("/task/list")
    assert response.status_code == 200
    tasks = response.json()
   # print(tasks)
    assert isinstance(tasks, list)

@pytest.mark.asyncio
async def test_delete_task(client):
    # Создаем задачу
    task_data = {"title": "Task to delete", "priority": 1}
    response = client.post("/task/create_task", json=task_data)
    task_id = response.json()["task_id"]

    # Удаляем задачу
    delete_response = client.delete(f"/task/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"
