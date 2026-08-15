````markdown
# Atlas

A modular backend platform for defining, executing, tracking, comparing, and reproducing computational experiments through a unified API.

---

# Project Overview

Atlas treats computational workloads as **Experiments** rather than tying the system to a specific type of workload such as machine learning.

An Experiment defines a plugin and its configuration. Each execution creates an independent **Run**, which is queued for asynchronous execution and stores its own configuration, lifecycle state, results, metrics, artifacts, and execution metadata.

The goal is to build the infrastructure around computational experiments while keeping the actual experiment logic modular and extensible.

---

# Features

- REST API built with FastAPI
- Experiment creation, retrieval, updating, and deletion
- Independent Runs for each experiment execution
- Explicit Run lifecycle with validated state transitions
- Asynchronous execution using Celery and Redis
- PostgreSQL persistence through SQLAlchemy
- Plugin registry and common plugin interface
- Per-run configuration snapshots
- Structured results and metrics
- Artifact tracking
- Execution timestamps and duration tracking
- Failure handling and `FAILED` Run states
- Run history for individual Experiments
- Run comparison
- Automated testing with Pytest

---

# Architecture

```text
                         Client
                           │
                           ▼
                     ┌───────────┐
                     │  FastAPI  │
                     │    API    │
                     └─────┬─────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │ PostgreSQL  │           │    Redis    │
       │  + SQLAlchemy│          │   Broker    │
       └─────────────┘           └──────┬──────┘
                                        │
                                        ▼
                                  ┌─────────────┐
                                  │   Celery    │
                                  │   Worker    │
                                  └──────┬──────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │   Plugins   │
                                  └─────────────┘
```

---

# Execution Pipeline

```text
Experiment
    │
    ▼
Create Run
    │
    ▼
QUEUED
    │
    ▼
RUNNING
    │
    ▼
Plugin Execution
    │
    ├── Result
    ├── Metrics
    └── Artifacts
    │
    ▼
COMPLETED
```

If execution fails:

```text
RUNNING → FAILED
```

Run state transitions are handled explicitly by the execution lifecycle, preventing invalid transitions.

---

# Plugin Architecture

Experiment-specific execution logic is separated from the core platform through a common plugin interface.

```python
class BasePlugin:

    def execute(self, config: dict) -> dict:
        ...
```

Plugins are resolved through a registry when a Run is executed.

This allows different computational workloads to share the same execution, tracking, and persistence pipeline without changing the core system.

Example plugin output:

```json
{
  "result": {
    "model": "LinearRegression"
  },
  "metrics": {
    "mse": 3.944304526105059e-31,
    "r2": 1
  },
  "artifacts": {
    "model": "artifacts/model.pkl"
  }
}
```

---

# Data Model

Atlas is centered around two main entities.

### Experiment

Defines a workload:

```text
Experiment
├── id
├── name
├── plugin
├── config
└── runs
```

### Run

Represents one execution:

```text
Run
├── id
├── experiment_id
├── status
├── created_at
├── started_at
├── completed_at
├── result
├── metrics
├── config
└── artifacts
```

Multiple Runs can belong to the same Experiment while remaining independently reproducible and comparable.

---

# API

## Experiments

```text
POST   /experiments/
GET    /experiments/
GET    /experiments/{experiment_id}
PUT    /experiments/{experiment_id}
DELETE /experiments/{experiment_id}
```

Example:

```json
{
  "name": "Linear Regression",
  "plugin": "ml",
  "config": {
    "test_size": 0.2,
    "random_state": 42
  }
}
```

## Runs

```text
POST /runs/
POST /runs/{run_id}/execute
GET  /runs/{run_id}
GET  /runs/experiment/{experiment_id}
GET  /runs/compare
```

Example completed Run:

```json
{
  "id": 8,
  "experiment_id": 2,
  "status": "COMPLETED",
  "result": {
    "model": "LinearRegression"
  },
  "metrics": {
    "mse": 3.944304526105059e-31,
    "r2": 1
  },
  "config": {
    "test_size": 0.2,
    "random_state": 42
  },
  "artifacts": {
    "model": "artifacts/model.pkl"
  },
  "duration_seconds": 0.064578
}
```

Interactive API documentation is available through FastAPI's Swagger UI.

---

# Project Structure

```text
atlas/
│
├── api/
│   ├── main.py
│   └── routers/
│       ├── experiments.py
│       └── runs.py
│
├── core/
│   ├── config/
│   ├── execution/
│   │   ├── lifecycle.py
│   │   ├── service.py
│   │   └── status.py
│   └── schemas/
│
├── database/
│   ├── base.py
│   ├── connection.py
│   ├── dependencies.py
│   ├── models.py
│   └── session.py
│
├── plugins/
│   ├── base.py
│   ├── registry.py
│   └── ...
│
├── workers/
│   └── tasks.py
│
├── tests/
│   ├── test_experiments.py
│   ├── test_plugins.py
│   └── test_run_lifecycle.py
│
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Task Queue | Celery |
| Message Broker | Redis |
| Infrastructure | Docker / Docker Compose |
| Testing | Pytest |

---

# Installation

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the required services:

```bash
docker compose up -d
```

---

# Run

Start the API:

```bash
python -m uvicorn api.main:app --reload
```

Start the Celery worker using the project's configured Celery application.

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Testing

Run the test suite:

```bash
pytest
```

The test suite covers:

- Experiment API behavior
- Plugin registration and execution
- Run creation
- Run lifecycle transitions
- Invalid state transitions
- Asynchronous execution
- Successful execution
- Failed execution
- Execution pipeline behavior

---

# Engineering Highlights

- **Modular execution** — workload-specific logic is isolated behind plugins.
- **Asynchronous processing** — long-running work is separated from API requests through Celery.
- **Explicit state management** — Run lifecycle transitions are validated rather than handled as arbitrary status updates.
- **Reproducibility** — configuration, results, metrics, artifacts, and execution metadata are retained for each Run.
- **Persistence** — experiments and their execution history are stored in PostgreSQL.
- **Extensibility** — new experiment types can be introduced through the plugin system without restructuring the core execution pipeline.
- **Testability** — core lifecycle and execution behavior is covered by automated tests.

---

# Future Improvements

- Experiment versioning
- Persistent artifact storage
- Richer Run comparison
- Additional plugins
- Authentication and authorization
- Cloud deployment

---

