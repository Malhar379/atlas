from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus
from workers.tasks import execute_run
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.dependencies import get_db
from database.models import Experiment, Run
from core.schemas.run import (
    RunCreate,
    RunResponse,
    RunComparisonResponse,
)


router = APIRouter(
    prefix="/runs",
    tags=["Runs"]
)


@router.post("/", response_model=RunResponse)
def create_run(
    run: RunCreate,
    db: Session = Depends(get_db)
):
    experiment = (
        db.query(Experiment)
        .filter(Experiment.id == run.experiment_id)
        .first()
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found"
        )

    db_run = Run(
    experiment_id=experiment.id,
    config=experiment.config,

    )

    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    return db_run

@router.post("/{run_id}/execute", response_model=RunResponse)
def start_run(
    run_id: int,
    db: Session = Depends(get_db)
):
    run = (
        db.query(Run)
        .filter(Run.id == run_id)
        .first()
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    try:
        new_status = transition_run(
            RunStatus(run.status),
            RunStatus.QUEUED,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    run.status = new_status.value

    db.commit()
    db.refresh(run)

    execute_run.delay(run.id)

    return run

@router.get("/compare", response_model=RunComparisonResponse)
def compare_runs(
    run_id_1: int,
    run_id_2: int,
    db: Session = Depends(get_db),
):
    run_1 = (
        db.query(Run)
        .filter(Run.id == run_id_1)
        .first()
    )

    run_2 = (
        db.query(Run)
        .filter(Run.id == run_id_2)
        .first()
    )

    if run_1 is None:
        raise HTTPException(
            status_code=404,
            detail=f"Run {run_id_1} not found"
        )

    if run_2 is None:
        raise HTTPException(
            status_code=404,
            detail=f"Run {run_id_2} not found"
        )

    return {
        "run_1": run_1,
        "run_2": run_2,
    }

@router.get("/{run_id}", response_model=RunResponse)
def get_run(
    run_id: int,
    db: Session = Depends(get_db)
):
    run = (
        db.query(Run)
        .filter(Run.id == run_id)
        .first()
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    return run

@router.get(
    "/experiment/{experiment_id}",
    response_model=List[RunResponse]
)
def get_experiment_runs(
    experiment_id: int,
    db: Session = Depends(get_db)
):
    runs = (
        db.query(Run)
        .filter(Run.experiment_id == experiment_id)
        .all()
    )

    return runs

