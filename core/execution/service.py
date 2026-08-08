from sqlalchemy.orm import Session

from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus
from database.models import Run


def update_run_status(
    run: Run,
    new_status: RunStatus,
    db: Session,
) -> Run:

    current_status = RunStatus(run.status)

    run.status = transition_run(
        current_status,
        new_status,
    ).value

    db.commit()
    db.refresh(run)

    return run