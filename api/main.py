from fastapi import FastAPI

app = FastAPI(
    title="Atlas",
    description="A Containerized Computational Experimentation Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Atlas is running"}