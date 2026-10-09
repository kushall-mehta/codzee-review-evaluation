from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Task Manager API")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class Task(TaskCreate):
    id: int
    completed: bool = False

tasks = {}
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Task Manager API is running"}

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate):
    global next_id
    task = Task(
        id=next_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
    )
    tasks[next_id] = task
    next_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = task.model_copy(update={"completed": True})
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return None

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = task.model_copy(
        update={
            "title": task_data.title,
            "description": task_data.description,
        }
    )

    tasks[task_id] = updated_task
    return updated_task
