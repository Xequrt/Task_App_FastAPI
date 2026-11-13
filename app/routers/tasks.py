from typing import Annotated

from fastapi import APIRouter, Response, status, HTTPException, Path
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

TaskData = dict[str, str | int | bool]

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[TaskData] = [
    {"id": 1, "title": "Изучить параметр пути", "completed": False, "tag": "work"},
    {"id": 2, "title": "Найти задачу", "completed": False, "tag": "study"},
]


@router.get("", response_class=HTMLResponse)
async def list_tasks(q: str | None = None) -> str:
    filtered_tasks = tasks
    if q is not None:
        normalized_query = q.casefold()
        filtered_tasks = [
            task for task in tasks if normalized_query in str(task["title"]).casefold()
        ]

    items = "".join(f"<li>{task['title']}</li>" for task in filtered_tasks)
    return f"<h1>Задачи</h1><ul>{items}</ul>"


@router.get("/tag/{name}", response_class=HTMLResponse)
async def show_tag(
    name: Annotated[str, Path(min_length=2)],
) -> str:
    filtered_tasks = tasks
    filtered_tasks = [
                task for task in tasks if task["tag"].casefold() == name.casefold()
            ]
    if filtered_tasks == []:
        raise HTTPException(status_code=404, detail="Task tag not found")
    items = "".join(f"<li>{task['title']}</li>" for task in filtered_tasks)
    return f"<h1>Задачи</h1><ul>{items}</ul>"

@router.get("/new", response_class=HTMLResponse)
async def new_task() -> str:
    return "<h1>Новая задача</h1>"

@router.get("/{task_id}", response_class=HTMLResponse)
async def show_task(
    task_id: Annotated[int, Path(gt=0)],
) -> str:
    for task in tasks:
        if task["id"] == task_id:
            return f"<h1>{task['title']}</h1>"

    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/count", response_class=PlainTextResponse, response_model=None)
async def task_count(q: str | None = None) -> str | Response:
    filtered_tasks = tasks
    if q is not None:
        normalized_query = q.casefold()
        filtered_tasks = [
            task for task in tasks if normalized_query in str(task["title"]).casefold()
        ]
    items_count = len(filtered_tasks)
    return str(items_count) if items_count != 0 else Response(status_code=204)

@router.get("/about", response_class=HTMLResponse)
async def about_tasks() -> str:
    return "<h1>Task App</h1><p>Список учебных задач</p>"

@router.get(
        "/info",
        response_class=HTMLResponse,
        status_code=status.HTTP_200_OK,
)
async def task_info(response: Response) -> str:
    response.headers["X-Tasks-Count"] = str(len(tasks))
    return f"<p>Всего задач {len(tasks)}</p>"

@router.get("/all")
async def redirect_to_tasks() -> RedirectResponse:
    return RedirectResponse(url="/tasks", status_code=307)

@router.post("")
async def create_task() -> dict[str, str]:
    return {"action": "create"}