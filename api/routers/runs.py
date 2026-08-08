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