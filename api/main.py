from fastapi import FastAPI

from api.routers.experiments import router as experiment_router
from api.routers.runs import router as run_router

app = FastAPI()

app.include_router(experiment_router)
app.include_router(run_router)


@app.get("/")
def root():
    return {"message": "Atlas is running"}