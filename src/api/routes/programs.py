"""Programs routes."""
from fastapi import APIRouter
router = APIRouter()

@router.get("/programs")
def list_programs():
    return []
