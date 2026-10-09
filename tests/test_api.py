from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_running_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Task Manager API is running"


def test_create_task_with_valid_input():
    response = client.post(
        "/tasks",
        json={"title": "Learn FastAPI", "description": "Build an API"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Learn FastAPI"


def test_create_task_trims_title():
    response = client.post(
        "/tasks",
        json={"title": "  Learn Python  "},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Learn Python"

def test_create_task_rejects_blank_title():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_rejects_long_title():
    response = client.post("/tasks", json={"title": "a" * 101})
    assert response.status_code == 422


def test_create_task_rejects_long_description():
    response = client.post(
        "/tasks",
        json={"title": "Valid title", "description": "a" * 501},
    )
    assert response.status_code == 422


def test_update_task():
    create_response = client.post(
        "/tasks",
        json={"title": "Old title", "description": "Old description"},
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New title", "description": "New description"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["description"] == "New description"


def test_update_missing_task():
    response = client.put(
        "/tasks/99999",
        json={"title": "New title", "description": "New description"},
    )

    assert response.status_code == 404


def test_complete_task():
    create_response = client.post(
        "/tasks",
        json={"title": "Complete me"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_missing_task():
    response = client.patch("/tasks/99999/complete")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={"title": "Delete me"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_missing_task():
    response = client.delete("/tasks/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
