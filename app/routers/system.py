from fastapi import APIRouter

router = APIRouter(prefix="/system")

@router.get("/status")
async def get_status() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/check")
async def check_status() -> dict[str, str]:
    return {"check": "started"}
