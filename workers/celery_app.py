from celery import Celery

celery_app = Celery(
    "atlas",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.imports = (
    "workers.tasks",
)

import workers.tasks