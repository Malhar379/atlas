from sqlalchemy.orm import Session

from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus
from plugins.registry import get_plugin
from database.models import Run

def update_run_status(
    run,
    new_status: RunStatus,
    db: Session,
):
    new_status = transition_run(
        RunStatus(run.status),
        new_status,
    )

    run.status = new_status.value

    db.commit()
    db.refresh(run)

    return run

def execute_run(db: Session, run_id: int):
    run = db.query(Run).filter(Run.id == run_id).first()

    if run is None:
        raise ValueError(f"Run {run_id} not found")

    # QUEUED -> RUNNING
    run.status = transition_run(
        RunStatus(run.status),
        RunStatus.RUNNING,
    ).value

    db.commit()
    db.refresh(run)

    try:
        plugin = get_plugin(run.experiment.plugin)

        result = plugin.execute({})

        # RUNNING -> COMPLETED
        run.status = transition_run(
            RunStatus(run.status),
            RunStatus.COMPLETED,
        ).value

        db.commit()
        db.refresh(run)

        return {
            "run_id": run.id,
            "status": run.status,
            "result": result,
        }

    except Exception:
        # RUNNING -> FAILED
        run.status = transition_run(
            RunStatus(run.status),
            RunStatus.FAILED,
        ).value

        db.commit()
        db.refresh(run)

        raise