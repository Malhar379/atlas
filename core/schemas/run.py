from datetime import datetime

from pydantic import BaseModel


class RunCreate(BaseModel):
    experiment_id: int


class RunResponse(BaseModel):
    id: int
    experiment_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True