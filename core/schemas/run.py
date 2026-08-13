from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import Any

class RunCreate(BaseModel):
    experiment_id: int


class RunResponse(BaseModel):
    id: int
    experiment_id: int
    status: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None
    metrics: dict | None = None
    config: dict | None
    artifacts: dict[str, Any] | None = None

    @computed_field
    @property
    def duration_seconds(self) -> float | None:
        if self.started_at is None or self.completed_at is None:
            return None

        return (self.completed_at - self.started_at).total_seconds()

    model_config = {
        "from_attributes": True
    }

class RunComparisonResponse(BaseModel):
    run_1: RunResponse
    run_2: RunResponse