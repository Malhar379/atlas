from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus
from workers.tasks import execute_run
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from database.models import Experiment, Run
from core.schemas.run import RunCreate, RunResponse


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
        experiment_id=run.experiment_id
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