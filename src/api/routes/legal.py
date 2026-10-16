"""Legal routes."""
from fastapi import APIRouter
router = APIRouter()

@router.get("/legal/{program_id}")
def get_legal(program_id: str):
    return {}
