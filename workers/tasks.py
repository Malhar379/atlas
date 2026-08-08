from workers.celery_app import celery_app

from database.connection import SessionLocal
from database.models import Run

from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus


@celery_app.task
def execute_run(run_id: int):
    db = SessionLocal()

    try:
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

        print(f"Executing run {run_id}")

        # Temporary plugin execution
        plugin_result = {
            "message": "Example plugin executed successfully",
            "config": {},

        }

        # Save result
        run.result = plugin_result

        # RUNNING -> COMPLETED
        run.status = transition_run(
            RunStatus(run.status),
            RunStatus.COMPLETED,
        ).value

        db.commit()
        db.refresh(run)

        return {
            "run_id": run_id,
            "status": run.status,
            "result": run.result,
        }

    except Exception as exc:
        db.rollback()

        run = db.query(Run).filter(Run.id == run_id).first()

        if run is not None:
            run.status = transition_run(
                RunStatus(run.status),
                RunStatus.FAILED,
            ).value

            run.result = {
                "error": str(exc),
            }

            db.commit()

        raise

    finally:
        db.close()