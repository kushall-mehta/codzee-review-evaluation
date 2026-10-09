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
