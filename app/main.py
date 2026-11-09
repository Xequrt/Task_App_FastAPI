from fastapi import FastAPI

from app.routers import tasks, system

app = FastAPI()
app.include_router(tasks.router)
app.include_router(system.router)


@app.get("/")
async def index() -> dict[str, str]:
    return {"name": "Task App", "status": "ok"}
