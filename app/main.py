from fastapi import FastAPI, Response

from app.routers import tasks, system

app = FastAPI()
app.include_router(tasks.router)
app.include_router(system.router)


@app.get("/")
async def index() -> dict[str, str]:
    return {"name": "Task App", "status": "ok"}

@app.get("/health")
async def health() -> Response:
    return Response(
        content="ok",
        media_type="text/plain",
        status_code=200,
    )
