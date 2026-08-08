from workers.celery_app import celery_app


@celery_app.task
def execute_run(run_id: int):
    print(f"Executing run {run_id}")

    return {
        "run_id": run_id,
        "status": "COMPLETED",
    }