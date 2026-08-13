from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from database.models import Experiment
from core.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
)

from core.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentUpdate,
)

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/", response_model=ExperimentResponse)
def create_experiment(
    experiment: ExperimentCreate,
    db: Session = Depends(get_db)
):
    db_experiment = Experiment(
        name=experiment.name,
        plugin=experiment.plugin,
        config=experiment.config
    )

    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)

    return db_experiment

@router.get("/", response_model=List[ExperimentResponse])
def get_experiments(
    db: Session = Depends(get_db)
):
    experiments = db.query(Experiment).all()
    return experiments

@router.get("/{experiment_id}", response_model=ExperimentResponse)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(get_db)
):
    experiment = (
        db.query(Experiment)
        .filter(Experiment.id == experiment_id)
        .first()
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found"
        )

    return experiment

@router.put("/{experiment_id}", response_model=ExperimentResponse)
def update_experiment(
    experiment_id: int,
    updated_experiment: ExperimentUpdate,
    db: Session = Depends(get_db)
):
    experiment = (
        db.query(Experiment)
        .filter(Experiment.id == experiment_id)
        .first()
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found"
        )

    experiment.name = updated_experiment.name
    experiment.plugin = updated_experiment.plugin
    experiment.config = updated_experiment.config

    db.commit()
    db.refresh(experiment)

    return experiment

@router.delete("/{experiment_id}")
def delete_experiment(
    experiment_id: int,
    db: Session = Depends(get_db)
):
    experiment = (
        db.query(Experiment)
        .filter(Experiment.id == experiment_id)
        .first()
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found"
        )

    db.delete(experiment)
    db.commit()

    return {"message": "Experiment deleted successfully"}

