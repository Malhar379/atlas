from datetime import datetime

from pydantic import BaseModel

from core.execution.status import RunStatus

from typing import Any

class RunCreate(BaseModel):
    experiment_id: int


class RunResponse(BaseModel):
    id: int
    experiment_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

from typing import Any

class RunResponse(BaseModel):
    id: int
    experiment_id: int
    status: RunStatus
    created_at: datetime
    result: Any | None = None