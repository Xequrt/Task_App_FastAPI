from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from app.routers import tasks, system

app = FastAPI()
app.include_router(tasks.router)
app.include_router(system.router)


@app.get("/")
async def index() -> dict[str, str]:
    return {"name": "Task App", "status": "ok"}

@app.get(
    "/projects/{project_id}/tasks/{task_id}",
    response_class=HTMLResponse,
)
async def show_project_task(project_id: int, task_id: int) -> str:
    return f"<p>Проект {project_id}, задача {task_id}</p>"

@app.get("/health")
async def health() -> Response:
    return Response(
        content="ok",
        media_type="text/plain",
        status_code=200,
    )
