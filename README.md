# Task Manager API

A small REST API built with FastAPI for creating and managing tasks. This project is the starting point for evaluating Codzee's pull-request code review experience.

## Features

- List all tasks
- Create a task
- Get a task by ID
- Mark a task as complete
- Delete a task
- Automatic interactive API documentation

## Requirements

- Python 3.10 or newer

## Setup

Create and activate a virtual environment:

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Health message |
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{task_id}` | Get one task |
| PATCH | `/tasks/{task_id}/complete` | Mark a task complete |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Notes

This starter version stores tasks in memory, so data resets whenever the application restarts. It is intended for learning and code-review evaluation, not production deployment.

## Codzee evaluation plan

Create separate branches and pull requests for meaningful improvements such as:

1. Input validation and edge-case handling
2. More robust API error handling and security-related validation
3. Automated tests and maintainability improvements

Record Codzee's actual findings, including accurate comments, false positives, and issues it misses. Do not claim a finding occurred unless you observed it.
