from pydantic import BaseModel, Field
from typing import Any


class ExperimentCreate(BaseModel):
    name: str
    plugin: str
    config: dict[str, Any] = Field(default_factory=dict)


class ExperimentResponse(BaseModel):
    id: int
    name: str
    plugin: str
    config: dict[str, Any]

    model_config = {
        "from_attributes": True
    }


class ExperimentUpdate(BaseModel):
    name: str
    plugin: str
    config: dict[str, Any] = Field(default_factory=dict)