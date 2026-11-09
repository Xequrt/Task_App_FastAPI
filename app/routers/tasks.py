from fastapi import APIRouter, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

TaskData = dict[str, str | int | bool]

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[TaskData] = [
    {"id": 1, "title": "Изучить запрос", "completed": False},
    {"id": 2, "title": "Сформировать ответ", "completed": False},
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

@router.get("/count", response_class=PlainTextResponse)
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