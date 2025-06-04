"""Tests for the /tasks endpoints
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task_success(async_client: AsyncClient):
    """Test creating a task successfully"""

    payload = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo",
        "priority": 1
    }

    response = await async_client.post("/tasks/", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]
    assert data["priority"] == payload["priority"]


@pytest.mark.asyncio
async def test_read_tasks_success(async_client: AsyncClient):
    """Test listing all tasks (with pagination)"""

    response = await async_client.get("/tasks/")
    data = response.json()

    assert response.status_code == 200
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_read_tasks_with_filter(async_client: AsyncClient):
    """Test filtering tasks by title and status"""

    response = await async_client.get("/tasks/", params={"title": "Test", "status": False})
    data = response.json()

    assert response.status_code == 200
    assert "items" in data

    for item in data["items"]:
        assert "Test" in item["title"]
        assert item["completed"] is False


@pytest.mark.asyncio
async def test_get_single_task_success(async_client: AsyncClient):
    """Test getting a task by ID"""

    payload = {
        "title": "Another Task",
        "description": "Single get test",
        "status": "in_progress",
        "priority": 2
    }
    create_response = await async_client.post("/tasks/", json=payload)
    task_id = create_response.json()["id"]
    response = await async_client.get(f"/tasks/{task_id}/")

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == task_id
    assert data["title"] == payload["title"]


@pytest.mark.asyncio
async def test_update_task_success(async_client: AsyncClient):
    """Test updating a task"""

    payload = {
        "title": "To Be Updated",
        "description": "Old desc",
        "status": "todo",
        "priority": 3
    }

    create_resp = await async_client.post("/tasks/", json=payload)
    task_id = create_resp.json()["id"]

    update_data = {"title": "Updated Title"}
    response = await async_client.put(f"/tasks/{task_id}/", json=update_data)
    updated = response.json()

    assert response.status_code == 200
    assert updated["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_task_success(async_client: AsyncClient):
    """Test deleting a task"""

    payload = {
        "title": "To Be Deleted",
        "description": "Delete me",
        "status": "todo",
        "priority": 4
    }

    create_resp = await async_client.post("/tasks/", json=payload)
    task_id = create_resp.json()["id"]

    # Delete the task
    response = await async_client.delete(f"/tasks/{task_id}/")
    assert response.status_code == 204

    # Ensure it's gone
    get_resp = await async_client.get(f"/tasks/{task_id}/")
    assert get_resp.status_code == 404
