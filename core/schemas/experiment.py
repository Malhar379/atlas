from pydantic import BaseModel


class ExperimentCreate(BaseModel):
    name: str
    plugin: str

class ExperimentResponse(BaseModel):
    id: int
    name: str
    plugin: str

    model_config = {
        "from_attributes": True
    }

class ExperimentUpdate(BaseModel):
    name: str
    plugin: str