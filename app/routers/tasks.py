from fastapi import APIRouter

router = APIRouter(prefix="/tasks")


@router.get("")
async def list_tasks() -> dict[str, str]:
    return {"action": "list"}


@router.post("")
async def create_task() -> dict[str, str]:
    return {"action": "create"}